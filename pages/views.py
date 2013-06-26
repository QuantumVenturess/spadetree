from django.shortcuts import render

def about(request):
    """About page."""
    d = {
        'title': 'About',
    }
    return render(request, 'pages/about.html', d)