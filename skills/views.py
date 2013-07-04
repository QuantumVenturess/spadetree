from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext

from interests.models import Interest
from sessions.decorators import sign_in_required
from skills.models import Skill
from spadetree.utils import add_csrf

import json

@sign_in_required
def delete(request, pk, format=None):
    """Delete skill with pk for user."""
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST' and request.user == skill.user:
        skill_pk = skill.pk
        skill.delete()
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
def new(request, format=None):
    """Create a new skill using a new or existing interest."""
    if request.method == 'POST' and request.POST.get('interest_name'):
        interest_name = request.POST.get('interest_name').lower()
        try:
            # Check to see if interest exists
            interest = Interest.objects.get(name=interest_name)
        except Interest.DoesNotExist:
            interest = Interest(name=interest_name)
            interest.save()
        try:
            # Check to see if user has this skill
            skill = request.user.skill_set.get(interest=interest)
            message = 'You already have this skill'
        except Skill.DoesNotExist:
            # If user does not have this skill, create it
            skill = request.user.skill_set.create(interest=interest)
            message = 'Skill added'
            if format:
                if format == '.js':
                    d = {
                        'skill': skill,
                        'static': settings.STATIC_URL,
                    }
                    skill_add_form = loader.get_template(
                        'skills/skill_add_form.html')
                    skill_delete_form = loader.get_template(
                        'skills/skill_delete_form.html')
                    context = RequestContext(request, add_csrf(request, d))
                    data = {
                        'skill_add_form': skill_add_form.render(context),
                        'skill_delete_form': skill_delete_form.render(context),
                    }
                    return HttpResponse(json.dumps(data), 
                        mimetype='application/json')
                elif format == '.json':
                    print 'JSON'
                    return HttpResponse('json')
        else:
            messages.success(request, message)
    return HttpResponseRedirect(reverse('users.views.edit',
        args=[request.user.profile.slug]))