from django.http import HttpResponse
from django.db.models import Q

from cities.models import City

import json
import operator

def city_list(request, name=None):
    """Display list of cities for autocomplete for user edit page for state."""
    query = request.GET.get('term')
    results = []
    if name and query:
        state_name = ' '.join(name.split('-')).lower()
        queries = [word for word in query.split(' ') if word]
        qs = [(Q(state__name=state_name) & 
            (Q(name=q) | Q(name__icontains=q))) for q in queries]
        results = City.objects.filter(reduce(operator.and_,
            qs)).order_by('name')[0:3]
    names = [city.name.title() for city in results]
    return HttpResponse(json.dumps(names), mimetype='application/json')