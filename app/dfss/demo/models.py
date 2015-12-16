from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class Resume(models.Model):
    user = models.ForeignKey(User)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    timestamp = models.TextField(null=True)
    latest_timestamp = models.DateTimeField(auto_now_add=True)
