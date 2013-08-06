from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from choices.models import Choice
from interests.models import Interest

class Channel(models.Model):
    choice   = models.ForeignKey(Choice, blank=True, null=True)
    created  = models.DateTimeField(auto_now_add=True)
    interest = models.ForeignKey(Interest, blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        unique_together = ('choice', 'interest',)

    def __unicode__(self):
        return unicode(self.pk)

    def create_notification(self, user, action):
        if self.choice:
            model = 'choice'
        elif self.interest:
            model = 'interest'
        self.notification_set.create(action=action, model=model, user=user)

    def notification_count(self):
        from notifications.models import Notification
        return Notification.objects.filter(channel=self).count()

    def subscription_count(self):
        from subscriptions.models import Subscription
        return Subscription.objects.filter(channel=self).count()

    def subscribe(self, user):
        try:
            subscription = self.subscription_set.get(user=user)
        except ObjectDoesNotExist:
            self.subscription_set.create(user=user)

    def unsubscribe(self, user):
        try:
            subscription = self.subscription_set.get(user=user)
            subscription.delete()
        except ObjectDoesNotExist:
            pass