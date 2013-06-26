from django.contrib.auth.models import User
from django.db import models

from interests.models import Interest

class Choice(models.Model):
    accepted       = models.BooleanField(default=False)
    completed      = models.BooleanField(default=False)
    created        = models.DateTimeField(auto_now_add=True)
    content        = models.TextField()
    date_completed = models.DateTimeField(blank=True, null=True)
    denied         = models.BooleanField(default=False)
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

    def date_completed_string(self):
        """Jun 20, 2013 for date_complete."""
        return self.date_completed.strftime('%b %d, %Y')

    def date_string(self):
        """Jun 20, 2013"""
        return self.created.strftime('%b %d, %Y')