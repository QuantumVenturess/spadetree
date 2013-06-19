from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext

from sessions.decorators import already_logged_in
from users.models import Profile
from utils.utils import add_csrf

import os, socket

@login_required
def choose(request):
    """If user has not chosen if they are a tutee or tutor."""
    if request.method == 'POST':
        profile = request.user.profile
        message = ''
        if request.POST.get('tutee'):
            # If user chooses to be a tutee
            profile.tutee = True
            profile.tutor = False
            message       = 'Start learning new skills'
        elif request.POST.get('tutor'):
            # If user chooses to be a tutor
            profile.tutee = False
            profile.tutor = True
            message       = 'Share your knowledge'
        profile.save()
        messages.success(request, message)
        return HttpResponseRedirect(reverse('users.views.detail',
            args=[request.user.profile.slug]))
    d = {
        'title': 'Tutee or Tutor',
    }
    return render(request, 'users/choose.html', add_csrf(request, d))

@login_required
def detail(request, slug):
    """User detail page."""
    profile = get_object_or_404(Profile, slug=slug)
    user    = profile.user
    d = {
        'title': user.username,
        'user': user,
    }
    return render(request, 'users/detail.html', d)

@already_logged_in()
def join(request):
    """View for users who are not signed in."""
    d = {
        'title': 'Welcome',
    }
    return render(request, 'users/join.html', add_csrf(request, d))