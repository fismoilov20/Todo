from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
    heading = models.CharField(max_length=150)
    date = models.DateTimeField(null=True, blank=True)
    details = models.CharField(max_length=300)
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='todos')
    def __str__(self) -> str:
        return f"{self.heading}, {self.user.username}"

