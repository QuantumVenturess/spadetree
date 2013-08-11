from django.conf import settings

import json
import requests

def send_push_notification_to_tutee(choice):
    """Send push notification to Parse for Tutee from Tutor."""
    name = '%s %s' % (choice.tutor.first_name.title(), 
        choice.tutor.last_name[0].title())
    message = '%s accepted your request' % name
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
    """Send push notification to Parse for Tutor from Tutee."""
    name = '%s %s' % (choice.tutee.first_name.title(), 
        choice.tutee.last_name[0].title())
    message = '%s sent you a request' % name
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