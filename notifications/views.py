from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader, RequestContext

from sessions.decorators import sign_in_required

import json

@sign_in_required
def count(request):
    """Return notification count."""
    n = request.user.profile.unviewed_notification_count()
    data = {
        'count': n,
    }
    return HttpResponse(json.dumps(data), mimetype='application/json')

@sign_in_required
def list(request):
    """Display all notifications."""
    d = {
        'title': 'Notifications',
    }
    return render(request, 'notifications/list.html', d)

@sign_in_required
def notifications(request, format=None):
    """Return all notifications via JS and JSON."""
    user = request.user
    notifications = user.profile.notifications()
    # Mark all unviewed notifications as viewed
    unviewed = [n for n in notifications if not n.viewed(user)]
    for notification in unviewed:
        notification.mark_viewed(user)
    if format and format == '.json':
        data = {
            'notifications': [n.to_json() for n in notifications],
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    notifications.sort(key=lambda x: x.created, reverse=True)
    # Group notifications by day
    dates = sorted(set([n.created_date_string_long() for n in notifications]),
        key=lambda n: datetime.strptime(n, '%B %d, %Y'), reverse=True)
    days = []
    for day in dates:
        ns = [n for n in notifications if n.created_date_string_long() == day]
        days.append((day, ns))
    if request.is_ajax():
        d = {
            'days': days,
        }
        t        = loader.get_template('notifications/notifications.html')
        context  = RequestContext(request, d)
        data = {
            'notifications': t.render(context),
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    return HttpResponseRedirect(reverse('root_path'))