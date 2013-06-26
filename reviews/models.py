from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Review(models.Model):
    content  = models.TextField()
    created  = models.DateTimeField(auto_now_add=True)
    positive = models.BooleanField(default=True)
    tutee    = models.ForeignKey(User, related_name='tutee_reviews')
    tutor    = models.ForeignKey(User, related_name='tutor_reviews')

    def __unicode__(self):
        return unicode(self.content)

    def date_string(self):
        """Jun 20, 2013"""
        return self.created.strftime('%b %d, %Y')

    def image_thumb(self):
        """Return thumbs up or thumbs down image."""
        direction = 'up' if self.positive else 'down'
        return '%simg/thumbs_%s.png' % (settings.STATIC_URL, direction)