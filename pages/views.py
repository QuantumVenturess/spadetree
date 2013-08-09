from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from interests.models import Interest

import json
import requests
import urllib
import urllib2

def about(request):
    """About page."""
    d = {
        'title': 'About SpadeTree',
    }
    return render(request, 'pages/about.html', d)

@csrf_exempt
def test(request):
    return HttpResponseRedirect(reverse('root_path'))