from django.db import models

# Create your models here.

class User(models.Model):
    objects = models.Manager()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __unicode__(self):
        return u'%s %s' % (self.username, self.password)