from datetime import datetime
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from cities.models import City
from oauth.models import Oauth
from oauth.utils import facebook_url
from sessions.decorators import already_signed_in
from states.models import State

import json
import pytz
import random
import re
import urllib2

@already_signed_in
def authenticate_app(request, format):
    if request.method == 'POST' and format == '.json':
        access_token  = request.POST.get('access_token')
        bio           = request.POST.get('bio')
        email         = request.POST.get('email')
        facebook_id   = request.POST.get('facebook_id')
        facebook_link = request.POST.get('facebook_link')
        first_name    = request.POST.get('first_name')
        last_name     = request.POST.get('last_name')
        location      = request.POST.get('location')
        username      = ' '.join([first_name, last_name])
        # Verification
        partial = 'CAAHhPEhKJfcBA' if not settings.DEV else 'CAACDp4ZA8AYsB'
        pattern = re.compile(partial)
        match   = re.search(pattern, access_token)
        print request.POST
        if match:
            print match
            # Check to see if oauth with facebook id exists
            try:
                oauth = Oauth.objects.get(facebook_id=facebook_id)
                # Update access token
                oauth.access_token = access_token
                oauth.facebook_link = link
                oauth.save()
                user = oauth.user
            # If oauth does not exist with that facebook id, create one
            except Oauth.DoesNotExist:
                # Check to see if user with email exists
                try:
                    user = User.objects.get(email=email)
                # If user with email does not exist
                except User.DoesNotExist:
                    # Lower case email
                    email = email.lower() if email else email
                    # Random password
                    letters = list(access_token)
                    random.shuffle(letters)
                    password = ''.join(letters[0:20])
                    user = User.objects.create(email=email, 
                        first_name=first_name, last_name=last_name, 
                            password=password, username=username)
                    # Set user profile attributes
                    profile = user.profile
                    profile.about = bio
                    if location and location.get('name'):
                        city_name, state_name = location.get('name').split(',')
                        city_name  = city_name.strip().lower()
                        state_name = state_name.strip().lower()
                        try:
                            # Check to see if state exists
                            state = State.objects.get(name=state_name)
                            try:
                                # Check to see if city exists in that state
                                city = state.city_set.get(name=city_name)
                            except City.DoesNotExist:
                                # If no city in that state exists, 
                                # create one in that state
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
                # Create oauth for user
                user.oauth_set.create(access_token=access_token, 
                    facebook_id=facebook_id, facebook_link=link, 
                        provider='facebook')
            if user:
                spadetree_token = '%s00000%s' % (user.pk, user.profile.token)
            else:
                spadetree_token = 'User did not save'
        else:
            spadetree_token = 'Invalid access token'
        data = {
            'id': user.pk,
            'spadetree_token': spadetree_token,
            'tutee': 1 if profile.tutee else 0,
            'tutor': 1 if profile.tutor else 0,
        }
        return HttpResponse(json.dumps(data), 
            mimetype='application/json')
    return HttpResponseRedirect(reverse('root_path'))

def facebook(request):
    return HttpResponseRedirect(facebook_url())

def facebook_authenticate(request):
    """Facebook sign up/sign in."""
    code  = request.GET.get('code')
    error = request.GET.get('error')
    # If the user cancels app permissions
    if error:
        messages.error(request, 'Unable to authenticate, please try again')
        # If user is not logged in
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse('users.view.join'))
        # If user is signed in
        else:
            # users.views.edit
            return HttpResponseRedirect(reverse('users.views.join'))
    # If user grants app permissions
    elif code:
        url = [
            'https://graph.facebook.com/oauth/access_token?',
            'client_id=%s&' % settings.FACEBOOK_APP_ID,
            'redirect_uri=%s&' % settings.FACEBOOK_REDIRECT_URI,
            'client_secret=%s&' % settings.FACEBOOK_APP_SECRET,
            'code=%s' % code
        ]
        # Combine url
        exchange = ''.join(url)
        response = urllib2.urlopen(exchange).read()
        access_token = response.split('=')[1].split('&')[0]
        graph = 'https://graph.facebook.com/me?access_token=%s' % access_token
        api_call = urllib2.urlopen(graph).read()
        # Extract data from json
        data        = json.loads(api_call)
        bio         = data.get('bio')
        email       = data.get('email')
        facebook_id = data.get('id')
        first_name  = data.get('first_name')
        last_name   = data.get('last_name')
        link        = data.get('link')
        location    = data.get('location')
        username    = ' '.join([first_name, last_name])
        # If user is not signed in
        if request.user.is_anonymous():
            # Check to see if oauth with facebook id exists
            try:
                oauth = Oauth.objects.get(facebook_id=facebook_id)
                # Update access token
                oauth.access_token  = access_token
                oauth.facebook_link = link
                oauth.save()
                user = oauth.user
            # If oauth does not exist with that facebook id, create one
            except ObjectDoesNotExist:
                # Check to see if user with email exists
                try:
                    user = User.objects.get(email=email)
                # If user with email does not exist
                except ObjectDoesNotExist:
                    # Lower case email
                    email = email.lower() if email else email
                    # Random password
                    letters = list(access_token)
                    random.shuffle(letters)
                    password = ''.join(letters[0:20])
                    user = User.objects.create(email=email, 
                        first_name=first_name, last_name=last_name, 
                            password=password, username=username)
                    # Set user profile attributes
                    profile = user.profile
                    profile.about = bio
                    if location and location.get('name'):
                        city_name, state_name = location.get('name').split(',')
                        city_name  = city_name.strip().lower()
                        state_name = state_name.strip().lower()
                        try:
                            # Check to see if state exists
                            state = State.objects.get(name=state_name)
                            try:
                                # Check to see if city exists in that state
                                city = state.city_set.get(name=city_name)
                            except City.DoesNotExist:
                                # If no city in that state exists, 
                                # create one in that state
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
                # Create oauth for user
                user.oauth_set.create(access_token=access_token, 
                    facebook_id=facebook_id, facebook_link=link, 
                        provider='facebook')
            # Sign in user
            auth.login(request, auth.authenticate(email=user.email))
        # If user is signed in
        else:
            # Check to see if oauth with facebook id exists
            try:
                oauth = request.user.oauth_set.get(facebook_id=facebook_id)
                # Update access token
                oauth.access_token = access_token
                oauth.save()
            # If oauth does not exist with facebook id, create one
            except ObjectDoesNotExist:
                request.user.oauth_set.create(access_token=access_token,
                    facebook_id=facebook_id, provider='facebook')
        # Redirect user
        if user.profile.has_chosen():
            if request.session.get('next'):
                # Friendly forwarding
                next = request.session['next']
                del request.session['next']
                return HttpResponseRedirect(next)
        else:
            # Redirect user to pick between tutee or tutor
            return HttpResponseRedirect(reverse('users.views.pick'))
    # If the user came straight to this URL
    if request.user.is_anonymous():
        return HttpResponseRedirect(reverse('users.views.join'))
    else:
        return HttpResponseRedirect(reverse('root_path'))