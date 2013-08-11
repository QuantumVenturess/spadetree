from django.conf import settings

import json
import requests

def send_push_notification_to_tutee(choice):
    """Send push notification to Parse for Tutee."""
    profile = choice.tutor.profile_set.all()[0]
    message = '%s accepted your request' % profile.full_name().title()
    payload = {
        'channels': ['choice_%s' % choice.pk],
        'data'    : {
            'alert'    : message,
            'badge'    : 'Increment',
            'choice_id': choice.pk,
        },
    }
    headers = {
        'X-Parse-Application-Id': settings.PARSE_APPLICATION_ID,
        'X-Parse-REST-API-Key'  : settings.PARSE_REST_API_KEY,
        'Content-Type'          : 'application/json',
    }
    r = requests.post(settings.PARSE_API_URL, data=json.dumps(payload),
        headers=headers)

def send_push_notification_to_tutor(choice):
    """Send push notification to Parse for Tutor."""
    profile = choice.tutee.profile_set.all()[0]
    message = '%s sent you a request' % profile.full_name().title()
    payload = {
        'channels': ['all_choices_user_%s' % choice.tutor.pk],
        'data'    : {
            'alert'    : message,
            'badge'    : 'Increment',
            'choice_id': choice.pk,
        },
    }
    headers = {
        'X-Parse-Application-Id': settings.PARSE_APPLICATION_ID,
        'X-Parse-REST-API-Key'  : settings.PARSE_REST_API_KEY,
        'Content-Type'          : 'application/json',
    }
    r = requests.post(settings.PARSE_API_URL, data=json.dumps(payload),
        headers=headers)