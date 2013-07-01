from datetime import datetime
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader, RequestContext

from choices.models import Choice
from sessions.decorators import sign_in_required
from spadetree.utils import add_csrf, page

import json
import pytz

@sign_in_required
def action(request, pk):
    """Accept, deny, or complete choice."""
    choice = get_object_or_404(Choice, pk=pk)
    if request.method == 'POST':
        action  = request.POST.get('action')
        # User is the tutor
        if request.user == choice.tutor:
            if action == 'accept':
                choice.accepted = True
                choice.denied   = False
            elif action == 'deny':
                choice.accepted = False
                choice.denied   = True
            # Change viewed status of choice
            choice.tutee_viewed = False # Mark tutee's request unviewed
            choice.tutor_viewed = True
        # User is the tutee
        elif request.user == choice.tutee:
            if action == 'complete' and choice.accepted and not choice.denied:
                choice.completed = True
                choice.date_completed = datetime.now(pytz.utc)
                # Mark request viewed for both tutee and tutor
                choice.tutee_viewed = True
                choice.tutor_viewed = True
        choice.save()
        if request.is_ajax():
            d = {
                'choice': choice,
            }
            choice_action_form = loader.get_template(
                'choices/choice_action_form.html')
            contact_number = loader.get_template('choices/contact_number.html')
            request_status = loader.get_template('choices/request_status.html')
            context = RequestContext(request, add_csrf(request, d))
            data = {
                'choice_action_form': choice_action_form.render(context),
                'choice_count': request.user.profile.choice_count(),
                'contact_number': contact_number.render(context),
                'pk': choice.pk,
                'request_status': request_status.render(context),
                'title_count': request.user.profile.title_count(),
            }
            return HttpResponse(json.dumps(data),
                mimetype='application/json')
        else:
            if choice.accepted:
                messages.success(request, 'Request accepted')
            elif choice.denied:
                messages.warning(request, 'Request denied')
            elif choice.completed:
                messages.success(request, 'Request completed')
    return HttpResponseRedirect(reverse('choices.views.requests'))

@sign_in_required
def requests(request):
    """Show all choices for tutee or tutor."""
    if request.user.profile.tutor:
        choices = request.user.tutor_choices.all().order_by('-created')
    else:
        choices = request.user.tutee_choices.all().order_by('-created')
        # Mark all unviewed requests for tutee as viewed
        for choice in choices.filter(tutee_viewed=False):
            choice.tutee_viewed = True
            choice.save()
    d = {
        'objects': page(request, choices),
        'title': 'Requests',
    }
    return render(request, 'choices/requests.html', add_csrf(request, d))