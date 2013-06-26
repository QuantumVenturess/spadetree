from django.db import models
from django.template.defaultfilters import slugify

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