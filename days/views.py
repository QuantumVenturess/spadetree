from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from days.models import Day, DayFree
from sessions.decorators import sign_in_required

import json

@sign_in_required
def free(request, pk):
    """User chose a day they are free."""
    day = get_object_or_404(Day, pk=pk)
    if request.method == 'POST':
        try:
            # If day free exists, delete it
            day_free = request.user.dayfree_set.get(day=day)
            day_free.delete()
        except DayFree.DoesNotExist:
            # If day free does not exist, create it
            day_free = request.user.dayfree_set.create(day=day)
    if request.is_ajax():
        return HttpResponse()
    return HttpResponseRedirect(reverse('users.views.edit',
        args=[request.user.profile.slug]))

@sign_in_required
@csrf_exempt
def free_value(request, value):
    """User chose a day they are free from app using day's value."""
    day = get_object_or_404(Day, value=value)
    if request.method == 'POST':
        try:
            # If day free exists, delete it
            day_free = request.user.dayfree_set.get(day=day)
            day_free.delete()
        except DayFree.DoesNotExist:
            # If day free does not exist, create it
            day_free = request.user.dayfree_set.create(day=day)
        data = {
            'day_free': day_free.to_json(),
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    return HttpResponseRedirect(reverse('users.views.edit',
        args=[request.user.profile.slug]))