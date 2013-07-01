from django.shortcuts import render

def about(request):
    """About page."""
    d = {
        'title': request.user.username,
    }
    return render(request, 'pages/about.html', d)