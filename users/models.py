from collections import defaultdict
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify

from cities.models import City
from usermessages.models import UserMessage

class Profile(models.Model):
    about    = models.TextField()
    city     = models.ForeignKey(City, blank=True, null=True)
    created  = models.DateTimeField(auto_now_add=True)
    image    = models.ImageField(blank=True, null=True, 
                   upload_to=settings.USER_IMAGE_URL)
    in_count = models.IntegerField(default=0)
    phone    = models.BigIntegerField(blank=True, null=True)
    slug     = models.SlugField(blank=True, null=True, max_length=255)
    tutee    = models.BooleanField(default=False)
    tutor    = models.BooleanField(default=False)
    user     = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.user)

    def choice_count(self):
        """Unviewed choices/requests count."""
        if self.tutor:
            return self.user.tutor_choices.filter(tutor_viewed=False).count()
        elif self.tutee:
            return self.user.tutee_choices.filter(tutee_viewed=False).count()

    def full_name(self):
        """Return full name if tutor or first name if tutee"""
        if self.tutor:
            return '%s %s' % (self.user.first_name, self.user.last_name)
        else:
            return self.user.first_name

    def has_chosen(self):
        if self.tutee or self.tutor:
            return True

    def image_big(self):
        if self.image:
            # return big image from amazon
            pass
        elif self.user.oauth_set.all():
            return 'http://graph.facebook.com/%s/picture?type=large' % (
                self.user.oauth_set.all()[0].facebook_id)
        else:
            return '%sdefault_big.jpg' % settings.USER_IMAGE_URL

    def image_small(self):
        if self.image:
            # return small image from amazon
            pass
        elif self.user.oauth_set.all():
            return 'http://graph.facebook.com/%s/picture' % (
                self.user.oauth_set.all()[0].facebook_id)
        else:
            return '%sdefault_small.jpg' % settings.USER_IMAGE_URL

    def interests(self):
        """Return interests from skills."""
        interests = [skill.interest for skill in self.user.skill_set.all()]
        interests.sort(key=lambda x: x.name)
        return interests

    def location(self):
        """Return city and state."""
        location = 'The World'
        if self.city:
            if self.city.state:
                location = '%s, %s' % (self.city, self.city.state)
            else:
                location = self.city
        return location

    def messages(self, sender):
        """All received and sent messages."""
        user_messages = UserMessage.objects.filter(
            Q(recipient=self.user, sender=sender) |
            Q(recipient=sender, sender=self.user))
        return user_messages

    def phone_string(self):
        """Return (408) 123-4567."""
        n = str(self.phone)
        if len(n) >= 10:
            return '(%s) %s-%s' % (n[0:3], n[3:6], n[6:10])
        else:
            return 'N/A'

    def recent_messages(self):
        """Return a list of the most recent messages."""
        messages = []
        user_messages = defaultdict(list)
        for msg in self.user.received_messages.all():
            user_messages[msg.sender].append(msg)
        for user, msgs in user_messages.items():
            most_recent = sorted(msgs, key=lambda x: x.created, reverse=True)[0]
            messages.append(most_recent)
        return sorted(messages, key=lambda x: x.created, reverse=True)

    def skills(self):
        """Return skills ordered by skill's interest's name."""
        return sorted(self.user.skill_set.all(), key=lambda x: x.interest.name)

    def skills_or_interests(self):
        """Return string Skills or Interests."""
        if self.tutor:
            return 'Skills'
        else:
            return 'Interests'

    def title_count(self):
        """Count number of unviewed choices/requests and user messages."""
        return self.choice_count() + self.unread_message_count()

    def token(self):
        """Use this to match with the token sent from iOS app."""
        try:
            oauth = self.user.oauth_set.all()[0]
            at    = oauth.access_token
            if at:
                return at[4] + at[8] + at[12] + at[21] + at[24]
        except IndexError:
            return

    def unread_message_count(self):
        """Count number of received messages that are unviewed."""
        unread_messages = self.user.received_messages.filter(viewed=False)
        unread_messages_set = set([msg.sender for msg in unread_messages])
        return len(unread_messages_set)

def update_profile(sender, instance, **kwargs):
    try:
        profile = Profile.objects.get(user=instance)
        profile.slug = slugify(instance.username)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(slug=slugify(instance.username), 
            user=instance)
    profile.in_count += 1
    profile.save()

# Create signals
post_save.connect(update_profile, sender=User)

# Enable user.profile() method
User.oauth   = property(lambda u: u.oauth_set.all()[0])
User.profile = property(lambda u: u.profile_set.all()[0])