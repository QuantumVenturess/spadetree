from cities.models import City
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify

class Profile(models.Model):
    about    = models.TextField()
    city     = models.ForeignKey(City, blank=True, null=True)
    created  = models.DateTimeField(auto_now_add=True)
    image    = models.ImageField(blank=True, null=True, 
                   upload_to=settings.USER_IMAGE_URL)
    in_count = models.IntegerField(default=0)
    slug     = models.SlugField(blank=True, null=True, max_length=255)
    tutee    = models.BooleanField(default=False)
    tutor    = models.BooleanField(default=False)
    user     = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.user)

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

def create_profile(sender, instance, **kwargs):
    try:
        profile = Profile.objects.get(user=instance)
        profile.slug = slugify(instance.username)
        profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(slug=slugify(instance.username), user=instance)

# Create signals
post_save.connect(create_profile, sender=User)

# Enable user.profile() method
User.profile = property(lambda u: u.profile_set.all()[0])