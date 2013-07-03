from django.contrib.auth.models import User
from django.db import models

from channels.models import Channel

class Subscription(models.Model):
    channel = models.ForeignKey(Channel)
    created = models.DateTimeField(auto_now_add=True)
    user    = models.ForeignKey(User)

    class Meta:
        ordering = ('-created',)
        unique_together = ('channel', 'user',)