from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader, RequestContext

from choices.models import Choice
from cities.models import City
from reviews.models import Review
from spadetree.utils import add_csrf, page
from states.models import State
from users.forms import ProfileForm
from users.models import Profile

import json
import os
import socket

@login_required
def choose(request, slug):
    """Tutee chooses tutor."""
    profile = get_object_or_404(Profile, slug=slug)
    if (request.method == 'POST' and profile.tutor and 
        request.user.profile.tutee):
    
        if request.POST.get('skill_pk'):
            user = profile.user
            try:
                skill = user.skill_set.all().get(pk=int(
                    request.POST.get('skill_pk')))
                content = request.POST.get('content')
                choice = Choice(content=content, interest=skill.interest, 
                    tutee=request.user, tutor=user)
                choice.save()
                if choice:
                    # Create user message
                    request.user.sent_messages.create(content=content,
                        recipient=user)
                messages.success(request, 
                    '%s has been sent your request to learn' % user.first_name)
                return HttpResponseRedirect(reverse('choices.views.requests'))
            except ObjectDoesNotExist:
                messages.error(request, 
                    '%s does not have that skill' % user.first_name)
    return HttpResponseRedirect(reverse('users.views.detail', 
        args=[profile.slug]))

@login_required
def detail(request, slug):
    """User detail page."""
    profile = get_object_or_404(Profile, slug=slug)
    if not profile.tutor and request.user != profile.user:
        messages.warning(request, 'You can only view tutors')
        return HttpResponseRedirect(reverse('users.views.detail', 
            args=[request.user.profile.slug]))
    user = profile.user
    reviews = user.tutor_reviews.all().order_by('-created')
    show_choice_button = (profile.tutor and request.user.profile.tutee and 
        profile.user != request.user)
    d = {
        'objects': page(request, reviews),
        'show_choice_button': show_choice_button,
        'skills': profile.skills(),
        'title': '%s %s' % (user.first_name, user.last_name),
        'userd': user,
    }
    if request.is_ajax():
        t = loader.get_template('reviews/reviews.html')
        p = loader.get_template('pagination.html')
        context = RequestContext(request, d)
        data = {
            'pagination': p.render(context),
            'results': t.render(context),
            'selector': '.userDetail .tutorReviews .prepend',
        }
        return HttpResponse(json.dumps(data),
            mimetype='application/json')
    return render(request, 'users/detail.html', d)

@login_required
def edit(request, slug):
    """Edit user page."""
    profile = get_object_or_404(Profile, slug=slug)
    user    = profile.user
    if request.user != user:
        return HttpResponseRedirect(reverse('users.views.edit',
            args=[request.user.profile.slug]))
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save()
        city_name  = request.POST.get('city_name')
        state_name = request.POST.get('state_name')
        if city_name and state_name:
            city_name  = city_name.lower()
            state_name = state_name.lower()
            try:
                # Check to see if state exists
                state = State.objects.get(name=state_name)
                try:
                    # Check to see if city exists in that state
                    city = state.city_set.get(name=city_name)
                except City.DoesNotExist:
                    # If no city in that state exists, create one in that state
                    city = City(name=city_name, state=state)
                    city.save()
            except State.DoesNotExist:
                # If state does not exist, create one
                state = State(name=state_name)
                state.save()
                # Then create a city for that state
                city = City(name=city_name, state=state)
                city.save()
            profile.city = city
            profile.save()
        messages.success(request, 'Profile updated')
        return HttpResponseRedirect(reverse('users.views.detail',
            args=[profile.slug]))
    profile_form = ProfileForm(instance=profile)
    skills = [skill for skill in user.skill_set.all()]
    d = {
        'profile_form': profile_form,
        'skills': sorted(skills, key=lambda x: x.interest.name),
        'title': 'Edit',
    }
    return render(request, 'users/edit.html', add_csrf(request, d))

@login_required
def new_review(request, slug, format=None):
    """Create new review for tutor."""
    profile = get_object_or_404(Profile, slug=slug)
    if request.method == 'POST':
        content = request.POST.get('content')
        # If current user is tutee and profile user is tutor
        if request.user.profile.tutee and profile.tutor and content:
            if request.POST.get('positive'):
                if int(request.POST.get('positive')):
                    positive = True
                else:
                    positive = False
            review = Review()
            review.content  = content
            review.positive = positive
            review.tutee    = request.user
            review.tutor    = profile.user
            review.save()
            if format:
                if format == '.js':
                    d = {
                        'review': review,
                        'static': settings.STATIC_URL,
                        'userd': profile.user,
                    }
                    new_review_form = loader.get_template(
                        'reviews/new_review_form.html')
                    review_template = loader.get_template(
                        'reviews/review.html')
                    context = RequestContext(request, add_csrf(request, d))
                    data = {
                        'new_review_form': new_review_form.render(context),
                        'review_template': review_template.render(context),
                    }
                    return HttpResponse(json.dumps(data),
                        mimetype='application/json')
                if format == '.json':
                    pass
            else:
                messages.success(request, 'Review submitted')
    return HttpResponseRedirect(reverse('users.views.detail',
        args=[profile.slug]))

@login_required
def pick(request):
    """If user has not picked if they are a tutee or tutor."""
    if request.method == 'POST':
        profile = request.user.profile
        message = ''
        if request.POST.get('tutee'):
            # If user chooses to be a tutee
            profile.tutee = True
            profile.tutor = False
            message       = 'Start learning new skills'
        elif request.POST.get('tutor'):
            # If user chooses to be a tutor
            profile.tutee = False
            profile.tutor = True
            message       = 'Share your knowledge'
        profile.save()
        messages.success(request, message)
        return HttpResponseRedirect(reverse('users.views.detail',
            args=[request.user.profile.slug]))
    d = {
        'title': 'Tutee or Tutor',
    }
    return render(request, 'users/pick.html', add_csrf(request, d))