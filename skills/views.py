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
    if request.method == 'POST' and request.POST.get('names'):
        names = request.POST.get('names').split(',')
        names = [name.strip().lower() for name in names]
        skills = []
        for name in names:
            try:
                # Check to see if interest exists
                interest = Interest.objects.get(name=name)
            except Interest.DoesNotExist:
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
                skills.append(skill)
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
        else:
            messages.success(request, message)
    return HttpResponseRedirect(reverse('users.views.edit',
        args=[request.user.profile.slug]))