from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from hours.models import Hour, HourFree
from sessions.decorators import sign_in_required

@sign_in_required
def free(request, pk):
    """Set free hour for user."""
    hour = get_object_or_404(Hour, pk=pk)
    if request.method == 'POST':
        try:
            # If hour free exists, delete it
            hour_free = request.user.hourfree_set.get(hour=hour)
            hour_free.delete()
        except HourFree.DoesNotExist:
            # If hour free does not exist, create it
            hour_free = request.user.hourfree_set.create(hour=hour)
    if request.is_ajax():
        return HttpResponse()
    return HttpResponseRedirect(reverse('users.views.edit',
        args=[request.user.profile.slug]))

@sign_in_required
@csrf_exempt
def free_value(request, value):
    """User chose an hour they are free from app using hour's value."""
    hour = get_object_or_404(Hour, value=value)
    if request.method == 'POST':
        try:
            # If hour free exists, delete it
            hour_free = request.user.hourfree_set.get(hour=hour)
            hour_free.delete()
        except HourFree.DoesNotExist:
            # If hour free does not exist, create it
            hour_free = request.user.hourfree_set.create(hour=hour)
        data = {
            'hour_free': hour_free.to_json(),
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    return HttpResponseRedirect(reverse('users.views.edit',
        args=[request.user.profile.slug]))