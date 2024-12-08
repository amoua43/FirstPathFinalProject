from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants= models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who created the project
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)  # Optional project link
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)  # The user posting the event
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    major = models.CharField(max_length=200)  # Related major
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# Added for job search
class Job(models.Model):
    jobtitle = models.CharField(max_length = 100)
    description = models.TextField(null = True, blank = True)
    location = models.TextField(null = True, blank = True)
    compname = models.TextField(null = True, blank = True)
    compdesc = models.TextField(null = True, blank = True)
    complocation = models.TextField(null = True, blank = True)

    def __str__(self):
        return self.jobtitle
