from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from hours.models import Hour, HourFree

@login_required
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