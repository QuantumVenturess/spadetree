from django.contrib import auth
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def sign_out(request):
    """Sign out."""
    auth.logout(request)
    return HttpResponseRedirect(reverse('users.views.join'))