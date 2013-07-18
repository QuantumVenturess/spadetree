from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext

from channels.models import Channel
from interests.models import Interest
from notifications.models import Notification
from sessions.decorators import sign_in_required
from skills.models import Skill
from spadetree.utils import add_csrf

import json
import re

@sign_in_required
def delete(request, pk, format=None):
    """Delete skill with pk for user."""
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST' and request.user == skill.user:
        interest = skill.interest
        skill_pk = skill.pk
        skill.delete()
        # Look for channel for interest
        try:
            channel = Channel.objects.get(interest=interest)
        except Channel.DoesNotExist:
            # Create the channel if it doesn't exist
            channel = Channel.objects.create(interest=interest)
        # Delete the notification for this channel from this user
        try:
            notification = channel.notification_set.get(user=request.user)
            notification.delete()
        except Notification.DoesNotExist:
            pass
        # Unsubscribe from channel
        channel.unsubscribe(request.user)
        if format:
            if format == '.js':
                data = {
                    'skill_pk': skill_pk,
                }
                return HttpResponse(json.dumps(data),
                    mimetype='application/json')
        else:
            messages.warning(request, 'Skill deleted')
    return HttpResponseRedirect(reverse('users.views.edit',
        args=[request.user.profile.slug]))

@sign_in_required
def delete_skill(request, pk):
    """Delete skill based on interest pk from app."""
    interest = get_object_or_404(Interest, pk=pk)
    try:
        skill = request.user.skill_set.get(interest=interest)
        skill.delete()
        # Look for channel for interest
        try:
            channel = Channel.objects.get(interest=interest)
        except Channel.DoesNotExist:
            # Create the channel if it doesn't exist
            channel = Channel.objects.create(interest=interest)
        # Delete the notification for this channel from this user
        try:
            notification = channel.notification_set.get(user=request.user)
            notification.delete()
        except Notification.DoesNotExist:
            pass
        # Unsubscribe from channel
        channel.unsubscribe(request.user)
        success = 1
    except Skill.DoesNotExist:
        success = 0
    data = {
        'success': success,
    }
    return HttpResponse(json.dumps(data), mimetype='application/json')

@sign_in_required
def new(request, format=None):
    """Create a new skill using a new or existing interest."""
    request_data = None
    if request.method == 'POST':
        request_data = request.POST
    elif format and format == '.json':
        request_data = request.GET
    if request_data and request_data.get('names'):
        names = request_data.get('names').split(',')
        skills = []
        json_skill = None
        for raw_name in names:
            raw_name = raw_name.strip().lower()
            name = re.sub('[^- \w]', '', raw_name)
            try:
                # Check to see if interest exists
                interest = Interest.objects.get(name=name)
            except Interest.DoesNotExist:
                # If interest does not exist, create one
                interest = Interest(name=name)
                interest.save()
            try:
                # Check to see if user has this skill
                skill = request.user.skill_set.get(interest=interest)
                message = 'You already have this skill'
            except Skill.DoesNotExist:
                # If user does not have this skill, create it
                skill = request.user.skill_set.create(interest=interest)
                message = 'Skill added'
                # Add multiple skills
                skills.append(skill)
                # Look for channel for interest
                try:
                    channel = Channel.objects.get(interest=interest)
                except Channel.DoesNotExist:
                    # Create the channel if it doesn't exist
                    channel = Channel.objects.create(interest=interest)
                # Post notification for this interest
                channel.create_notification(request.user, 'new')
                # Subscribe to channel for this interest
                channel.subscribe(request.user)
            json_skill = skill
        if format:
            if format == '.js':
                skill_add_form = loader.get_template(
                    'skills/skill_add_form.html')
                context = RequestContext(request, add_csrf(request, 
                    { 'static': settings.STATIC_URL }))
                forms = []
                for skill in skills:
                    skill_dict = {
                        'skill': skill,
                        'static': settings.STATIC_URL,
                    }
                    form = loader.get_template('skills/skill_delete_form.html')
                    c = RequestContext(request, add_csrf(request, skill_dict))
                    forms.append(form.render(c))
                data = {
                    'skill_add_form': skill_add_form.render(context),
                    'skill_delete_forms': ''.join(forms),
                }
                return HttpResponse(json.dumps(data), 
                    mimetype='application/json')
            elif format == '.json':
                data = {}
                if json_skill:
                    data['interest'] = json_skill.interest.to_json()
                return HttpResponse(json.dumps(data),
                    mimetype='application/json')
        else:
            messages.success(request, message)
    return HttpResponseRedirect(reverse('users.views.edit',
        args=[request.user.profile.slug]))