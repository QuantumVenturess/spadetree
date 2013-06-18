from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from utils.utils import add_csrf
import os, socket

def join(request):
    """View for users who are not signed in."""
    d = {
        'title': 'Welcome',
    }
    return render(request, 'users/join.html', add_csrf(request, d));