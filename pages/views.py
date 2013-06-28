from django.shortcuts import render

from sessions.decorators import sign_in_required

@sign_in_required
def about(request):
    """About page."""
    d = {
        'title': request.user.username,
    }
    return render(request, 'pages/about.html', d)