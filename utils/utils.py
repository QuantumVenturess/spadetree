from django.core.context_processors import csrf

def add_csrf(request, dictionary):
  dictionary.update(csrf(request))
  return dictionary