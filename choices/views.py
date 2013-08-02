from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt

from channels.models import Channel
from cities.models import City
from choices.models import Choice, ChoiceNote
from notifications.models import Notification
from sessions.decorators import sign_in_required
from spadetree.utils import add_csrf, page
from states.models import State

import json
import pytz

@sign_in_required
@csrf_exempt
def action(request, pk, format=None):
    """Accept, deny, or complete choice."""
    choice = get_object_or_404(Choice, pk=pk)
    if request.method == 'POST':
        action  = request.POST.get('action')
        # User is the tutor
        if request.user == choice.tutor:
            if action == 'accept':
                choice.accepted = True
                choice.denied   = False
                try:
                    channel = Channel.objects.get(choice=choice)
                    # Subscribe user to channel with this choice
                    channel.subscribe(request.user)
                    # Create notification for this channel
                    channel.create_notification(request.user, 'accept')
                except Channel.DoesNotExist:
                    pass
            elif action == 'deny':
                choice.accepted = False
                choice.denied   = True
                try:
                    channel = Channel.objects.get(choice=choice)
                    # Unsubscribe user from channel with this choice
                    channel.unsubscribe(request.user)
                    # Create notification for this channel
                    channel.create_notification(request.user, 'deny')
                except Channel.DoesNotExist:
                    pass
            # Change viewed status of choice
            # choice.tutee_viewed = False # Mark tutee's request unviewed
            choice.tutor_viewed = True
        # User is the tutee
        elif request.user == choice.tutee:
            if action == 'complete' and choice.accepted and not choice.denied:
                choice.completed = True
                choice.date_completed = datetime.now(pytz.utc)
                # Mark request viewed for both tutee and tutor
                choice.tutee_viewed = True
                choice.tutor_viewed = True
                try:
                    channel = Channel.objects.get(choice=choice)
                    # Create notification for this channel
                    channel.create_notification(request.user, 'complete')
                except Channel.DoesNotExist:
                    pass
        choice.save()
        if format and format == '.json':
            data = {
                'choice': choice.to_json(),
            }
        elif request.is_ajax():
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
        if (format and format == '.json') or request.is_ajax():
            return HttpResponse(json.dumps(data),
                mimetype='application/json')
        if choice.accepted:
            messages.success(request, 'Request accepted')
        elif choice.denied:
            messages.warning(request, 'Request denied')
        elif choice.completed:
            messages.success(request, 'Request completed')
    return HttpResponseRedirect(reverse('choices.views.requests'))

@sign_in_required
def count(request):
    """Return request count."""
    n = request.user.profile.choice_count()
    return HttpResponse(json.dumps(n), mimetype='application/json')

@sign_in_required
def detail(request, pk):
    """Detail page for choice/request."""
    choice = get_object_or_404(Choice, pk=pk)
    if not request.user in [choice.tutee, choice.tutor]:
        messages.error(request, 'This is not your request')
        return HttpResponseRedirect(reverse('choices.views.requests'))
    if request.method == 'POST' and request.user.profile.tutee:
        date       = request.POST.get('date')
        address    = request.POST.get('address')
        city_name  = request.POST.get('city_name')
        state_name = request.POST.get('state_name')
        try:
            month, day, year = date.split('/')
        except ValueError:
            date = None
        if date and address and city_name and state_name:
            date = datetime(int(year), int(month), int(day))
            address    = address.lower()
            city_name  = city_name.lower()
            state_name = state_name.lower()
            try:
                state = State.objects.get(name=state_name)
            except State.DoesNotExist:
                state = State(name=state_name)
                state.save()
            try:
                city = state.city_set.get(name=city_name)
            except City.DoesNotExist:
                city = City(name=city_name, state=state)
                city.save()
            choice.address = address
            choice.city    = city
            choice.state   = state
            if choice.day.value == int(date.strftime('%w')):
                choice.date = date
                messages.success(request, 
                    'Tutor has been notified of your date and place')
                # Create notification for channel with this choice
                try:
                    channel = Channel.objects.get(choice=choice)
                    channel.create_notification(request.user, 'update')
                except Channel.DoesNotExist:
                    pass
            else:
                messages.error(request, 
                    'Date must be a %s' % choice.day.name.title())
            choice.save()
    d = {
        'choice': choice,
        'choice_notes': choice.choicenote_set.all().order_by('-created'),
        'title': '%s on %s at %s' % (choice.interest.name.title(),
            choice.day.name.title(), choice.hour.time_string()),
    }
    return render(request, 'choices/detail.html', add_csrf(request, d))

@sign_in_required
def new_note(request, pk):
    """Create a new note for choice."""
    choice = get_object_or_404(Choice, pk=pk)
    if request.user not in [choice.tutee, choice.tutor]:
        return HttpResponseRedirect(reverse('choices.views.requests'))
    if request.method == 'POST' and request.POST.get('content'):
        choice_note = ChoiceNote(choice=choice, 
            content=request.POST.get('content'), user=request.user)
        choice_note.save()
        try:
            channel = Channel.objects.get(choice=choice)
            # Create notification for this channel
            notification = Notification()
            notification.action      = 'new'
            notification.channel     = channel
            notification.choice_note = choice_note
            notification.model       = 'choice_note'
            notification.user        = request.user
            notification.save()
        except Channel.DoesNotExist:
            pass
        if request.is_ajax():
            d = {
                'choice': choice,
                'choice_note': choice_note,
            }
            choice_note_template = loader.get_template(
                'choices/choice_note.html')
            choice_note_form = loader.get_template(
                'choices/choice_note_form.html')
            context = RequestContext(request, add_csrf(request, d))
            data = {
                'choice_note_template': choice_note_template.render(
                    context),
                'choice_note_form': choice_note_form.render(context)
            }
            return HttpResponse(json.dumps(data),
                mimetype='application/json')
    return HttpResponseRedirect(reverse('choices.views.detail',
        args=[choice.pk]))

@sign_in_required
def requests(request, format=None):
    """Show all choices for tutee or tutor."""
    if request.user.profile.tutor:
        choices = request.user.tutor_choices.all().order_by('-created')
    else:
        choices = request.user.tutee_choices.all().order_by('-created')
        # Mark all unviewed requests for tutee as viewed
        for choice in choices.filter(tutee_viewed=False):
            choice.tutee_viewed = True
            choice.save()
    paged = page(request, choices, 5)
    if format and format =='.json':
        data = {
            'choices': [choice.to_json() for choice in paged],
            'pages'  : paged.paginator.num_pages,
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    d = {
        'objects': paged,
        'title'  : 'Requests',
    }
    return render(request, 'choices/requests.html', add_csrf(request, d))