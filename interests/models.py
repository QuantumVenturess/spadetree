from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify

from spadetree.utils import nsdate_format

class Interest(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name    = models.CharField(max_length=255, unique=True)
    slug    = models.SlugField(blank=True, null=True, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.slug = slugify(self.name)
        super(Interest, self).save(*args, **kwargs)

    def to_json(self):
        """Convert model to json serializable."""
        dictionary = {
            'created': nsdate_format(self.created),
            'name': self.name,
            'pk': self.pk,
            'slug': self.slug,
        }
        return dictionary

def create_channel(sender, instance, **kwargs):
    from channels.models import Channel
    try:
        channel = Channel.objects.get(interest=instance)
    except Channel.DoesNotExist:
        Channel.objects.create(interest=instance)

# Create a for each interest after it saves
post_save.connect(create_channel, sender=Interest)