from django.contrib.auth.models import User
from django.db import models

from spadetree.utils import nsdate_format

class UserMessage(models.Model):
    created   = models.DateTimeField(auto_now_add=True)
    content   = models.TextField()
    recipient = models.ForeignKey(User, related_name='received_messages')
    sender    = models.ForeignKey(User, related_name='sent_messages')
    viewed    = models.BooleanField(default=False)

    def __unicode__(self):
        return 'To: %s, From: %s' % (self.recipient.profile.full_name(),
            self.sender.profile.full_name())

    class Meta:
        ordering = ('-created',)

    def date(self):
        return self.created.strftime('%b %d, %y')

    def date_time(self):
        return '%s at %s' % (self.date(), self.time())

    def time(self):
        time = self.created.strftime('%I:%M').lstrip('0')
        am_pm = self.created.strftime('%p').lower()
        return time + am_pm

    def to_json(self):
        dictionary = {
            'created'  : nsdate_format(self.created),
            'content'  : self.content,
            'id'       : self.pk,
            'recipient': self.recipient.profile.to_json(),
            'sender'   : self.sender.profile.to_json(),
            'viewed'   : 1 if self.viewed else 0,
        }
        return dictionary