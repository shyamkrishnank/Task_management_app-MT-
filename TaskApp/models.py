from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=120, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

status_choices = [
    ('Incomplete', 'Incomplete'),
    ('Complete', 'Complete'),
]


class Tasks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=30, choices=status_choices, default='Incomplete')