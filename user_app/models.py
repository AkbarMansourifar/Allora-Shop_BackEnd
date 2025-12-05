from django.db import models
from django.utils import timezone


class Ban(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.email} - {self.phone}"
