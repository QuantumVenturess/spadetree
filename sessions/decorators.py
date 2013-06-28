from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from functools import wraps

def already_logged_in():
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

def sign_in_required(function):
    def wrapper(request, *args, **kwargs):
        token = None
        if request.method == 'GET':
            token = request.GET.get('spadetree_token')
        elif request.method == 'POST':
            token = request.POST.get('spadetree_token')
        if token and len(token.split('00000')) == 2:
            pk, token = token.split('00000')
            try:
                user = User.objects.get(pk=pk)
                if user.profile.token() != token:
                    user = None
            except User.DoesNotExist:
                user = None
        else:
            user = request.user
        if user and user.id:
            request.user = user
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('sessions.views.join'))
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