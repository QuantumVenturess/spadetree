from django.db import models
from django.template.defaultfilters import slugify

from states.models import State

class City(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name    = models.CharField(max_length=255)
    slug    = models.SlugField(blank=True, max_length=255, null=True)
    state   = models.ForeignKey(State)

    class Meta:
        ordering        = ('name',)
        unique_together = ('name', 'state',)

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)

    def to_json(self):
        dictionary = {
            'id': self.pk,
            'name': self.name,
            'slug': self.slug,
            'state': self.state.to_json(),
        }
        return dictionary