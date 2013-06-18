from django.conf import settings

import random

def facebook_url():
    state = ''.join([str(random.randrange(0, 10)) for i in range(0, 10)])
    url =[
        'https://www.facebook.com/dialog/oauth?',
        'client_id=%s&' % settings.FACEBOOK_APP_ID,
        'redirect_uri=%s&' % settings.FACEBOOK_REDIRECT_URI,
        'scope=%s&' % settings.FACEBOOK_SCOPE,
        'state=%s' 
    ]
    return ''.join(url)