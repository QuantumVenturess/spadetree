from django.contrib.auth.models import User
from django.db import models

class Hour(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    value   = models.IntegerField(unique=True)

    class Meta:
        ordering = ('value',)

    def __unicode__(self):
        return unicode(self.value)

    def am_pm(self):
        if self.value < 12:
            return 'am'
        else:
            return 'pm'

    def hour_of_day(self):
        if self.value > 0:
            if self.value > 12:
                return self.value - 12
            else:
                return self.value
        else:
            return 12

    def time_string(self):
        return '%s %s' % (self.hour_of_day(), self.am_pm())

    def to_json(self):
        dictionary = {
            'uid': self.pk,
            'value': self.value,
        }
        return dictionary

class HourFree(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    hour    = models.ForeignKey(Hour)
    user    = models.ForeignKey(User)

    class Meta:
        ordering = ('hour__value',)
        unique_together = ('hour', 'user',)

    def __unicode__(self):
        return 'User: %s, Hour: %s' % (self.user, self.hour)