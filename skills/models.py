from django.contrib.auth.models import User
from django.db import models
from interests.models import Interest

class Skill(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    interest = models.ForeignKey(Interest)
    user     = models.ForeignKey(User)

    class Meta:
        unique_together = ('interest', 'user',)

    def __unicode__(self):
        return 'User: %s, Interest: %s' % (self.user, self.interest)