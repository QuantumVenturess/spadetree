from django.core.context_processors import csrf
from django.core.paginator import EmptyPage, InvalidPage, Paginator

from spadetree.digg_paginator import DiggPaginator

def add_csrf(request, dictionary):
    dictionary.update(csrf(request))
    return dictionary

def page(request, objects, per_page=None):
    """Create paginator object and return it."""
    # [leading block] [current page] [trailing block]
    # body is the size of the block that contains the currently active page
    # margin defines the minimum number of pages required between two blocks
    # tail is the number of pages in the leading and trailing blocks
    if not per_page:
        # Default per page
        per_page = 10
    paginator = DiggPaginator(objects, per_page, body=5, margin=1, tail=0)
    try:
        page = int(request.GET.get('p', '1'))
    except ValueError:
        page = 1
    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)
    return items