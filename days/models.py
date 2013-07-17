from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

class Day(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name    = models.CharField(max_length=255, unique=True)
    slug    = models.SlugField(blank=True, null=True, max_length=255)
    value   = models.IntegerField(unique=True)

    class Meta:
        ordering = ('value',)

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.slug = slugify(self.name)
        super(Day, self).save(*args, **kwargs)

    def to_json(self):
        dictionary = {
            'id': self.pk,
            'name': self.name,
            'value': self.value,
        }
        return dictionary

class DayFree(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    day     = models.ForeignKey(Day)
    user    = models.ForeignKey(User)

    class Meta:
        ordering = ('day__value',)
        unique_together = ('day', 'user',)

    def __unicode__(self):
        return 'User: %s, Day: %s' % (self.user, self.day)

    def to_json(self):
        dictionary = {
            'day': self.day.to_json(),
            'id': self.pk,
        }
        return dictionary