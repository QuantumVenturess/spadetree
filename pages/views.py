from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from interests.models import Interest

import json

def about(request):
    """About page."""
    d = {
        'title': 'About SpadeTree',
    }
    return render(request, 'pages/about.html', d)

@csrf_exempt
def test(request):
    method = 'GET'
    if request.method == 'POST':
        name = request.POST.get('name')
        print name
        if name:
            method = name
        else:
            method = 'POST'
    data = {
        'method': method,
    }
    print method
    return HttpResponse(json.dumps(data), 
        mimetype='application/json')