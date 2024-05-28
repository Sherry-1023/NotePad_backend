from django.db import models

# Create your models here.

class User(models.Model):
    objects = models.Manager()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.username

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=100)
    tags = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='notes/images/', blank=True, null=True)
    audio = models.FileField(upload_to='notes/audios/', blank=True, null=True)
    video = models.FileField(upload_to='notes/videos/', blank=True, null=True)

    def __str__(self):
        return self.title