from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from channels.models import Channel
from choices.models import ChoiceNote
from spadetree.utils import nsdate_format

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

    def choice_messages(self, url_link):
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
                return 'marked the %s for %s complete' % (self.model_link(
                    url_link), choice.interest.name.title())
            else:
                return '%s %s %s for %s' % (messages.get(self.action), pronoun, 
                    self.model_link(url_link), choice.interest.name.title())

    def created_date_string_long(self):
        """January 01, 2013."""
        return self.created.strftime('%B %d, %Y')

    def interest_messages(self, url_link):
        interest = self.channel.interest
        if interest:
            profile = self.user.profile
            word = 'a skill'
            if profile.tutee:
                word = 'an interest'
            messages = {
                'new': 'added %s as %s' % (self.model_link(url_link), word),
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

    def message(self, url_link=True):
        notification_messages = {
            'choice': self.choice_messages(url_link),
            'choice_note': self.choice_messages(url_link),
            'interest': self.interest_messages(url_link),
        }
        return notification_messages.get(self.model)

    def model_link(self, url_link):
        channel  = self.channel
        choice   = channel.choice
        interest = channel.interest
        link = ''
        if choice:
            link = '<a href="%s">request</a>' % reverse('choices.views.detail', 
                args=[choice.pk])
            if not url_link:
                link = 'request'
        elif interest:
            link = '<a href="%s">%s</a>' % (reverse('interests.views.detail', 
                args=[interest.slug]), interest.name.title())
            if not url_link:
                link = interest.name.title()
        return link

    def time(self):
        time = self.created.strftime('%I:%M').lstrip('0')
        am_pm = self.created.strftime('%p').lower()
        return '%s %s' % (time, am_pm)

    def to_json(self):
        channel  = self.channel
        choice   = None
        interest = None
        if self.model == 'choice':
            choice = channel.choice.to_json()
        if self.model == 'choice_note':
            choice = self.choice_note.choice.to_json()
        if self.model == 'interest':
            interest = channel.interest.to_json()
        dictionary = {
            'choice'  : choice,
            'created' : nsdate_format(self.created),
            'id'      : self.pk,
            'interest': interest,
            'message' : self.message(url_link=False),
            'user'    : self.user.profile.to_json(),

        }
        return dictionary

    def viewed(self, user):
        """Check to see if user has viewed this notification."""
        user_ids = self.users_viewed
        if user_ids:
            user_ids = [int(i) for i in user_ids.split(',')]
            if user.pk in user_ids:
                return True
        return False