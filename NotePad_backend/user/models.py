from django.db import models

# Create your models here.

class User(models.Model):
    objects = models.Manager()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=100, blank=True, null=True)
    def __unicode__(self):
        return u'%s %s' % (self.username, self.password)