from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader, RequestContext
from itertools import groupby

from interests.models import Interest
from interests.utils import group_interests_by_letter
from sessions.decorators import sign_in_required
from skills.models import Skill
from spadetree.utils import add_csrf, page

import json
import operator

@sign_in_required
def browse(request):
    """List of all interests grouped by letter for browsing."""
    interests = Interest.objects.all().order_by('name')
    paged     = page(request, interests, 20)
    groups    = group_interests_by_letter(paged)
    d = {
        'groups': groups,
        'objects': paged,
        'title': 'Browse',
    }
    if request.is_ajax():
        t = loader.get_template('interests/browse_results.html')
        p = loader.get_template('pagination.html')
        context = RequestContext(request, d)
        data = {
            'pagination': p.render(context),
            'results': t.render(context),
            'selector': '.interestList .results',
        }
        return HttpResponse(json.dumps(data),
            mimetype='application/json')
    return render(request, 'interests/browse.html', add_csrf(request, d))

@sign_in_required
def browse_search(request, format=None):
    """Return search results for browse."""
    query = request.GET.get('q')
    if query:
        queries = [word for word in query.split(' ') if word]
        qs = [(Q(name=q) | Q(name__icontains=q)) for q in queries]
        results = Interest.objects.all().filter(reduce(operator.and_, 
            qs)).order_by('name')
    else:
        results = Interest.objects.all().order_by('name')
    d = {
        'groups': group_interests_by_letter(results),
    }
    if format:
        if format == '.js':
            t = loader.get_template('interests/browse_results.html')
            context = RequestContext(request, d)
            data = {
                'browse_results': t.render(context),
            }
            return HttpResponse(json.dumps(data), mimetype='application/json')
    else:
        return HttpResponseRedirect(reverse('interests.views.browse'))

@sign_in_required
def detail(request, slug):
    """Detail page for interest."""
    interest = get_object_or_404(Interest, slug=slug)
    skills   = Skill.objects.filter(interest=interest)
    users    = [skill.user for skill in skills if skill.user.profile.tutor]
    users.sort(key=lambda x: x.first_name)
    d = {
        'interest': interest,
        'objects': page(request, users, 20),
        'title': interest.name.title(),
    }
    if request.is_ajax():
        tutors  = loader.get_template('interests/tutors.html')
        context = RequestContext(request, {
            'objects': users,
        });
        data = {
            'pk': interest.pk,
            'tutors': tutors.render(context),
        }
        return HttpResponse(json.dumps(data),
            mimetype='application/json')
    return render(request, 'interests/detail.html', d)

@sign_in_required
def search(request, format=None):
    """Return search results for interests."""
    query = request.GET.get('q')
    if query:
        queries = [word for word in query.split(' ') if word]
        qs = [(Q(name=q) | Q(name__icontains=q)) for q in queries]
        results = Interest.objects.all().filter(reduce(operator.and_, 
            qs)).order_by('name')[0:10]
    else:
        results = []
    if format:
        if format == '.js':
            t = loader.get_template('interests/results.html')
            context = RequestContext(request, { 'results': results })
            data = {
                'results': t.render(context),
            }
            return HttpResponse(json.dumps(data), mimetype='application/json')
    return HttpResponseRedirect(reverse('root_path'))