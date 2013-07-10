from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render

from sessions.decorators import sign_in_required

import json

@sign_in_required
def count(request):
    """Return notification count."""
    n = request.user.profile.unviewed_notification_count()
    return HttpResponse(json.dumps(n), mimetype='application/json')

@sign_in_required
def list(request):
    """Display all notifications."""
    user = request.user
    notifications = user.profile.notifications()
    notifications.sort(key=lambda x: x.created, reverse=True)
    # Group notifications by day
    dates = sorted(set([n.created_date_string_long() for n in notifications]),
        key=lambda n: datetime.strptime(n, '%B %d, %Y'), reverse=True)
    days = []
    for day in dates:
        ns = [n for n in notifications if n.created_date_string_long() == day]
        days.append((day, ns))
    # Mark all unviewed notifications as viewed
    unviewed = [n for n in notifications if not n.viewed(user)]
    for notification in unviewed:
        notification.mark_viewed(user)
    d = {
        'days': days,
        'title': 'Notifications',
    }
    return render(request, 'notifications/list.html', d)