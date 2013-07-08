from django.http import HttpResponse
from django.db.models import Q

from states.models import State

import json
import operator

def state_list(request):
    """Display list of states for autocomplete for user edit page."""
    query = request.GET.get('term')
    if query:
        queries = [word for word in query.split(' ') if word]
        qs = [(Q(name=q) | Q(name__icontains=q)) for q in queries]
        results = State.objects.filter(reduce(operator.and_, 
            qs)).order_by('name')[0:3]
    else:
        results = State.objects.all().order_by('name')[0:3]
    names = [state.name.title() for state in results]
    return HttpResponse(json.dumps(names), mimetype='application/json')