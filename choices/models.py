from django.contrib.auth.models import User
from django.db import models

from cities.models import City
from days.models import Day
from hours.models import Hour
from interests.models import Interest
from spadetree.utils import nsdate_format

class Choice(models.Model):
    accepted       = models.BooleanField(default=False)
    address        = models.CharField(blank=True, null=True, max_length=255)
    city           = models.ForeignKey(City, blank=True, null=True)
    completed      = models.BooleanField(default=False)
    created        = models.DateTimeField(auto_now_add=True)
    content        = models.TextField()
    date           = models.DateTimeField(blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)
    day            = models.ForeignKey(Day)
    denied         = models.BooleanField(default=False)
    hour           = models.ForeignKey(Hour)
    interest       = models.ForeignKey(Interest)
    tutee          = models.ForeignKey(User, related_name='tutee_choices')
    tutee_viewed   = models.BooleanField(default=True)
    tutor          = models.ForeignKey(User, related_name='tutor_choices')
    tutor_viewed   = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return 'Tutor: %s, Tutee: %s, Interest: %s' % (self.tutor.username, 
            self.tutee.username, self.interest.name.title())

    def created_date_string(self):
        """Jun 2, 13"""
        day   = self.created.strftime('%d').lstrip('0')
        month = self.created.strftime('%b')
        year  = self.created.strftime('%y')
        return '%s %s, %s' % (month, day, year)

    def date_completed_string(self):
        """Jun 2, 13"""
        day   = self.date_completed.strftime('%d').lstrip('0')
        month = self.date_completed.strftime('%b')
        year  = self.date_completed.strftime('%y')
        return '%s %s, %s' % (month, day, year)

    def date_string_long(self):
        """July 13, 2013"""
        if self.date:
            return self.date.strftime('%B %d, %Y')
        else:
            return '%s has not specified an exact date' % self.tutee.first_name

    def datepicker_string(self):
        """07/01/2013"""
        if self.date:
            return self.date.strftime('%m/%d/%Y')
        else:
            return ''

    def ready(self):
        """Choice is ready if it has a date, address, city, state, and zip."""
        if self.address and self.date and self.city:
            return True

    def state(self):
        return self.city.state.name.title()

    def to_json(self):
        dictionary = {
            'accepted' : 1 if self.accepted else 0,
            'address'  : self.address,
            'city'     : self.city.to_json() if self.city else '',
            'completed': 1 if self.completed else 0,
            'created'  : nsdate_format(self.created),
            'content'  : self.content,
            'date'     : nsdate_format(self.date) if self.date else '',
            'date_completed': nsdate_format(
                self.date_completed) if self.date_completed else '',
            'day'         : self.day.to_json(),
            'denied'      : 1 if self.denied else 0,
            'hour'        : self.hour.to_json(),
            'interest'    : self.interest.to_json(),
            'tutee'       : self.tutee.profile.to_json(),
            'tutee_viewed': 1 if self.tutee_viewed else 0,
            'tutor'       : self.tutor.profile.to_json(),
            'tutor_viewed': 1 if self.tutor_viewed else 0,
        }
        return dictionary

class ChoiceNote(models.Model):
    choice  = models.ForeignKey(Choice)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    user    = models.ForeignKey(User)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return '%s: %s' % (self.user, self.content)

    def created_date_string(self):
        """Jun 20, 13"""
        day   = self.created.strftime('%d').lstrip('0')
        month = self.created.strftime('%b')
        year  = self.created.strftime('%y')
        return '%s %s, %s' % (month, day, year)

    def date_time(self):
        """Jun 2, 13 at 7:00 am"""
        return '%s at %s' % (self.created_date_string(), self.time())

    def time(self):
        time  = self.created.strftime('%I:%M').lstrip('0')
        am_pm = self.created.strftime('%p').lower()
        return time + am_pm