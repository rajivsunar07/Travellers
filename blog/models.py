from django.db import models
from datetime import datetime, date
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import math

# Create your models here.

class Location(models.Model):
    country = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    address = models.TextField(max_length=255)

class Blog(models.Model):
    content = models.TextField()
    image = models.FileField(null=True, blank=True, upload_to='post_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        db_table = "Blog"
        ordering = ["-date_posted"]
    

