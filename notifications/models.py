from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from channels.models import Channel
from choices.models import ChoiceNote

class Notification(models.Model):
    action       = models.CharField(max_length=255)
    channel      = models.ForeignKey(Channel)
    choice_note  = models.ForeignKey(ChoiceNote, blank=True, null=True)
    created      = models.DateTimeField(auto_now_add=True)
    model        = models.CharField(max_length=255)
    user         = models.ForeignKey(User)
    users_viewed = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def choice_messages(self):
        choice = self.channel.choice
        if choice:
            profile = self.user.profile
            if profile.tutor:
                pronoun = 'your'
            elif profile.tutee:
                pronoun = 'the'
            messages = {
                'accept': 'accepted',
                'deny': 'denied',
                'new': 'added a note to',
                'update': 'updated',
            }
            if self.action == 'complete':
                return 'marked the %s for %s complete' % (self.model_link(),
                    choice.interest.name.title())
            else:
                return '%s %s %s for %s' % (messages.get(self.action), pronoun, 
                    self.model_link(), choice.interest.name.title())

    def created_date_string_long(self):
        """January 01, 2013."""
        return self.created.strftime('%B %d, %Y')

    def interest_messages(self):
        interest = self.channel.interest
        if interest:
            profile = self.user.profile
            if profile.tutor:
                word = 'a skill'
            elif profile.tutee:
                word = 'an interest'
            messages = {
                'new': 'added %s as %s' % (self.model_link(), word),
            }
            return messages.get(self.action)

    def mark_viewed(self, user):
        """Mark notification viewed for user."""
        user_ids = self.users_viewed
        if user_ids:
            user_ids = [int(i) for i in user_ids.split(',')]
            if not self.viewed(user):
                user_ids.append(user.pk)
                self.users_viewed = ','.join([str(i) for i in user_ids])
        else:
            self.users_viewed = '%s' % user.pk
        self.save()

    def message(self):
        notification_messages = {
            'choice': self.choice_messages(),
            'choice_note': self.choice_messages(),
            'interest': self.interest_messages(),
        }
        return notification_messages.get(self.model)

    def model_link(self):
        channel  = self.channel
        choice   = channel.choice
        interest = channel.interest
        link = ''
        if choice:
            link = '<a href="%s">request</a>' % reverse('choices.views.detail',
                args=[choice.pk])
        elif interest:
            link = '<a href="%s">%s</a>' % (reverse('interests.views.detail', 
                args=[interest.slug]), interest.name.title())
        return link

    def time(self):
        time = self.created.strftime('%I:%M').lstrip('0')
        am_pm = self.created.strftime('%p').lower()
        return '%s %s' % (time, am_pm)

    def viewed(self, user):
        """Check to see if user has viewed this notification."""
        user_ids = self.users_viewed
        if user_ids:
            user_ids = [int(i) for i in user_ids.split(',')]
            if user.pk in user_ids:
                return True
        return False