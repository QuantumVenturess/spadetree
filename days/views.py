from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from days.models import Day, DayFree

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