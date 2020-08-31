from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class User(AbstractUser):
    pass

class Priority(models.Model):
    type = models.CharField(max_length = 64)
    def __str__(self):
        return f"{self.type}"

class Task(models.Model):
    title = models.CharField(max_length = 64)
    description = models.CharField(max_length = 300)
    dateadd = models.DateField(default = datetime.datetime.now())
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "tasks")
    priority = models.ForeignKey(Priority, on_delete = models.CASCADE, related_name = "tasks")
    done = models.BooleanField(default = False)
    datecomp = models.DateField(null = True, blank = True)
    datedue = models.DateField(null = True, blank = True)
    def __str__(self):
        return f"{self.title}"
