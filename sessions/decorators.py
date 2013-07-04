from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import available_attrs
from functools import wraps

import urlparse

def already_signed_in(function):
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('_auth_user_id')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                return HttpResponseRedirect(reverse('users.views.detail',
                    args=[user.profile.slug]))
            except User.DoesNotExist:
                pass
        return function(request, *args, **kwargs)
    return wrapper

def staff_user():
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            user_id = request.session.get('_auth_user_id')
            if user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    if user.is_staff:
                        return func(request, *args, **kwargs)
                except ObjectDoesNotExist:
                    pass
            return HttpResponseRedirect(reverse('users.views.join'))
        return wraps(func)(inner_decorator)
    return decorator

def sign_in_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, 
    login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test_custom(
        lambda u: u.is_authenticated(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def user_passes_test_custom(test_func, login_url=None, 
    redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):

            user = request.user
            if user.is_authenticated():
                return view_func(request, *args, **kwargs)
            else:
                token = None
                if request.method == 'GET':
                    token = request.GET.get('spadetree_token')
                elif request.method == 'POST':
                    token = request.POST.get('spadetree_token')
                if token and len(token.split('00000')) == 2:
                    pk, token = token.split('00000')
                    try:
                        user = User.objects.get(pk=pk)
                        if user.profile.token() == token:
                            request.user = user
                            return view_func(request, *args, **kwargs)
                    except User.DoesNotExist:
                        pass

            # if test_func(request.user):
            #     return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse.urlparse(login_url or
                                                        settings.LOGIN_URL)[:2]
            current_scheme, current_netloc = urlparse.urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(path, login_url, redirect_field_name)
        return _wrapped_view
    return decorator

def already_signed_in_old():
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            user_id = request.session.get('_auth_user_id')
            if user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    return HttpResponseRedirect(reverse(
                        'users.views.detail', args=[user.profile.slug]))
                except ObjectDoesNotExist:
                    return func(request, *args, **kwargs)
            else:
                return func(request, *args, **kwargs)
        return wraps(func)(inner_decorator)
    return decorator

def sign_in_required_old(function):
    def wrapper(request, *args, **kwargs):
        # token = None
        # if request.method == 'GET':
        #     token = request.GET.get('spadetree_token')
        # elif request.method == 'POST':
        #     token = request.POST.get('spadetree_token')
        # if token and len(token.split('00000')) == 2:
        #     pk, token = token.split('00000')
        #     try:
        #         user = User.objects.get(pk=pk)
        #         if user.profile.token() != token:
        #             user = None
        #     except User.DoesNotExist:
        #         user = None
        # else:
        #     user = request.user
        user = request.user
        if user and user.id:
            # if token:
            #     request.user = user
            # if not user.profile.tutee and not user.profile.tutor:
            #     return HttpResponseRedirect(reverse('users.views.pick'))
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('sessions.views.join'))
    return wrapper