from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from sessions.decorators import already_logged_in

@already_logged_in()
def join(request):
    """View for users who are not signed in."""
    d = {
        'title': 'SpadeTree',
    }
    return render(request, 'sessions/join.html', d)

@login_required
def sign_out(request):
    """Sign out."""
    auth.logout(request)
    return HttpResponseRedirect(reverse('sessions.views.join'))