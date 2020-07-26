from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import reverse

# Create your models here.

class Request(models.Model):
    objects = models.Manager()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    text = models.TextField()
    created_date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['status']

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('request_merge')


class Comment(models.Model):
    post = models.ForeignKey('cs.Request', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class Notion(models.Model):
    post = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.post