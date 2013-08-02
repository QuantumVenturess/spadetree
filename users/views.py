from collections import defaultdict
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt

from choices.models import Choice
from cities.models import City
from days.models import Day, DayFree
from hours.models import Hour, HourFree
from oauth.models import Oauth
from reviews.models import Review
from sessions.decorators import sign_in_required
from spadetree.utils import add_csrf, page
from states.models import State
from users.forms import ProfileForm
from users.models import Profile

import json
import os
import socket
import urllib2

@sign_in_required
@csrf_exempt
def choose(request, slug, format=None):
    """Tutee chooses tutor."""
    profile = get_object_or_404(Profile, slug=slug)
    if (request.method == 'POST' 
        and profile.tutor and request.user.profile.tutee):

        content      = request.POST.get('content')
        day_free_pk  = request.POST.get('day_free_pk')
        hour_free_pk = request.POST.get('hour_free_pk')
        interest_pk  = request.POST.get('interest_pk')
        skill_pk     = request.POST.get('skill_pk')
        if ((interest_pk or skill_pk) 
            and day_free_pk and hour_free_pk and content):

            user = profile.user
            if interest_pk:
                try:
                    skill = user.skill_set.get(interest__pk=interest_pk)
                except Skill.DoesNotExist:
                    skill = None
            elif skill_pk:
                try:
                    skill = user.skill_set.get(pk=skill_pk)
                except Skill.DoesNotExist:
                    skill = None
            try:
                day_free = user.dayfree_set.get(pk=day_free_pk)
            except DayFree.DoesNotExist:
                day_free = None
            try:
                hour_free = user.hourfree_set.get(pk=hour_free_pk)
            except HourFree.DoesNotExist:
                hour_free = None
            if skill and day_free and hour_free:
                choice = Choice()
                choice.content  = content
                choice.day      = day_free.day
                choice.hour     = hour_free.hour
                choice.interest = skill.interest
                choice.tutee    = request.user
                choice.tutor    = user
                choice.save()
                if choice:
                    # Create channel for this choice
                    channel = choice.channel_set.create()
                    # Subscribe tutee to newly created channel
                    channel.subscribe(request.user)
                    # Create user message
                    request.user.sent_messages.create(content=content,
                        recipient=user, viewed=True)
                    if format == '.json':
                        data = {
                            'choice': choice.to_json(),
                        }
                        return HttpResponse(json.dumps(data),
                            mimetype='application/json')
                    else:
                        messages.success(request, 
                            """Set the day you want to start learning
                            and the place you want to meet""")
                        return HttpResponseRedirect(reverse(
                            'choices.views.detail', args=[choice.pk]))
    return HttpResponseRedirect(reverse('users.views.detail', 
        args=[profile.slug]))

@sign_in_required
def detail(request, slug, format=None):
    """User detail page."""
    profile = get_object_or_404(Profile, slug=slug)
    # If user has not picked to be a tutee or tutor
    if not profile.has_chosen():
        return HttpResponseRedirect(reverse('users.views.pick'))
    # You cannot view a tutee's page
    # if not profile.tutor and request.user != profile.user:
    #     messages.warning(request, 'You can only view tutors')
    #     return HttpResponseRedirect(reverse('users.views.detail', 
    #         args=[request.user.profile.slug]))
    user = profile.user
    show_choice_button = (profile.tutor and request.user.profile.tutee and 
        profile.user != request.user)
    days_free     = []
    hours_free_am = []
    hours_free_pm = []
    if show_choice_button:
        days_free     = user.dayfree_set.all().order_by('day__value')
        hours_free    = user.hourfree_set.all()
        hours_free_am = hours_free.filter(hour__value__gte=0, 
            hour__value__lte=11).order_by('hour__value')
        hours_free_pm = hours_free.filter(hour__value__gte=12,
            hour__value__lte=23).order_by('hour__value')
    if format and format == '.json':
        data = {
            'days_free': [free.to_json() for free in days_free],
            'hours_free_am': [free.to_json() for free in hours_free_am],
            'hours_free_pm': [free.to_json() for free in hours_free_pm],
            'skills': [skill.interest.to_json() for skill in profile.skills()],
            'user': profile.to_json(),
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    reviews = user.tutor_reviews.all().order_by('-created')
    user_is_tutor = profile.tutor
    d = {
        'days_free': days_free,
        'hours_free_am': hours_free_am,
        'hours_free_pm': hours_free_pm,
        'objects': page(request, reviews),
        'show_choice_button': show_choice_button,
        'skills': profile.skills(),
        'title': profile.full_name(),
        'user_is_tutor': user_is_tutor,
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

@sign_in_required
@csrf_exempt
def edit(request, slug, format=None):
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
            if request.POST.get('phone'):
                profile.phone = request.POST.get('phone')[0:10]
                profile.save()
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
        if format and format == '.json':
            data = {
                'user': profile.to_json(),
            }
            return HttpResponse(json.dumps(data), mimetype='application/json')
        messages.success(request, 'Profile updated')
        return HttpResponseRedirect(reverse('users.views.detail',
            args=[profile.slug]))
    days     = []
    day_ids  = [dayfree.day.pk for dayfree in user.dayfree_set.all()]
    hours_am = []
    hours_pm = []
    hour_ids = [hourfree.hour.pk for hourfree in user.hourfree_set.all()]
    if profile.tutor:
        for day in Day.objects.filter(value__gte=0, value__lte=6):
            button_class = ''
            if day.pk in day_ids:
                button_class = 'selected'
            days.append((day, button_class))
        for hour in Hour.objects.filter(value__gte=0, value__lte=23):
            button_class = ''
            if hour.pk in hour_ids:
                button_class = 'selected'
            if hour.value >= 0 and hour.value <= 11:
                hours_am.append((hour, button_class))
            elif hour.value >= 12 and hour.value <= 23:
                hours_pm.append((hour, button_class))
        hours_am.sort(key=lambda (x, c): x.value)
        hours_pm.sort(key=lambda (x, c): x.value)
    profile_form = ProfileForm(instance=profile)
    skills = [skill for skill in user.skill_set.all()]
    # Autocomplete source for city name
    if profile.city and profile.city.state:
        state_slug = profile.city.state.name.replace(' ', '-')
        city_autocomplete_source = reverse('cities.views.city_list',
            args=[state_slug])
    else:
        city_autocomplete_source = reverse('cities.views.city_list')
    d = {
        'city_autocomplete_source': city_autocomplete_source,
        'days': days,
        'hours_am': hours_am,
        'hours_pm': hours_pm,
        'profile_form': profile_form,
        'skills': sorted(skills, key=lambda x: x.interest.name),
        'title': 'Edit',
    }
    return render(request, 'users/edit.html', add_csrf(request, d))

@sign_in_required
def friends_tutored(request, slug, format=None):
    """Get a list of friends that this tutor has tutored."""
    profile = get_object_or_404(Profile, slug=slug)
    user    = profile.user
    oauth   = request.user.oauth
    if oauth and (format or request.is_ajax()):
        # Fetch Facebook friends
        url = 'https://graph.facebook.com/%s/friends/?access_token=%s' % (
            oauth.facebook_id, oauth.access_token)
        req         = urllib2.Request(url)
        response    = urllib2.urlopen(req)
        json_string = response.read()
        # Convert json string into dictionary
        json_dict = json.loads(json_string)
        # Get the value for key 'data', which is an array of user names and ids
        data_list = json_dict.get('data')
        # Create a list of Facebook ids
        facebook_ids = [d.get('id') for d in data_list]
        oauths       = Oauth.objects.filter(facebook_id__in=facebook_ids)
        users        = [oauth.user for oauth in oauths if oauth.user != user]
        # Create friend and choices tuple; (User, [choice1, choice2])
        friends = []
        groups  = []
        for u in users:
            group_dict = {
                'interests': [],
                'user'     : u.profile.to_json(),
            }
            choices = u.tutee_choices.filter(Q(accepted=True, tutor=user) | 
                Q(completed=True, tutor=user))
            if choices:
                choices   = sorted(list(choices), key=lambda x: x.interest.name)
                interests = []
                for choice in choices:
                    interest = choice.interest
                    interests.append(interest)
                    group_dict['interests'].append(interest.to_json())
                friends.append((u, interests))
                groups.append(group_dict)
        if format and format == '.json':
            data = {
                'groups': groups,
            }
        if request.is_ajax():
            d = {
                'friends': friends,
                'userd'  : profile.user,
            }
            t = loader.get_template('users/friends_tutored.html')
            context = RequestContext(request, d)
            data = {
                'friends_tutored': t.render(context),
            }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    return HttpResponseRedirect(reverse('root_path'))

@sign_in_required
@csrf_exempt
def new_review(request, slug, format=None):
    """Create new review for tutor."""
    profile = get_object_or_404(Profile, slug=slug)
    if request.method == 'POST':
        content = request.POST.get('content')
        # If current user is tutee and profile user is tutor and content
        if request.user.profile.tutee and profile.tutor and content:
            if request.POST.get('positive'):
                if int(request.POST.get('positive')):
                    positive = True
                else:
                    positive = False
            review          = Review()
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
                elif format == '.json':
                    data = {
                        'review': review.to_json(),
                    }
                return HttpResponse(json.dumps(data), 
                    mimetype='application/json')
            else:
                messages.success(request, 'Review submitted')
    return HttpResponseRedirect(reverse('users.views.detail',
        args=[profile.slug]))

@sign_in_required
@csrf_exempt
def pick(request, format=None):
    """If user has not picked if they are a tutee or tutor."""
    if request.user.profile.tutee or request.user.profile.tutor:
        return HttpResponseRedirect(reverse('users.views.detail',
            args=[request.user.profile.slug]))
    if request.method == 'POST':
        profile  = request.user.profile
        message  = ''
        redirect = reverse('root_path')
        if request.POST.get('tutor'):
            # If user chooses to be a tutor
            profile.tutee = False
            profile.tutor = True
            message       = 'Add your skills and update your info'
            redirect      = reverse('users.views.edit', args=[profile.slug])
        elif request.POST.get('tutee'):
            # If user chooses to be a tutee
            profile.tutee = True
            profile.tutor = False
            message       = 'Search for your interests and learn new skills'
            redirect      = reverse('interests.views.browse')
        profile.save()
        if format:
            if format == '.json':
                data = {
                    'tutee': 1 if profile.tutee else 0,
                    'tutor': 1 if profile.tutor else 0,
                }
                return HttpResponse(json.dumps(data), 
                    mimetype='application/json')
        messages.success(request, message)
        return HttpResponseRedirect(redirect)
    d = {
        'title': 'Tutee or Tutor',
    }
    return render(request, 'users/pick.html', add_csrf(request, d))

@sign_in_required
def reviews(request, slug):
    """Return all reviews for user."""
    profile = get_object_or_404(Profile, slug=slug)
    data = {}
    if profile.tutor:
        reviews = profile.user.tutor_reviews.all().order_by('-created')
        data = {
            'reviews': [review.to_json() for review in reviews],
        }
    return HttpResponse(json.dumps(data), mimetype='application/json')

@sign_in_required
def title_count(request):
    """Return total count of notifications, requests, and messages."""
    profile = request.user.profile
    n = profile.unviewed_notification_count()
    r = profile.choice_count()
    m = profile.unread_message_count()
    t = n + r + m
    return HttpResponse(json.dumps(t), mimetype='application/json')