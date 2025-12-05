from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=255)
    stock = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)

    variants = models.JSONField(default=list, blank=True)
    images = models.JSONField(default=list, blank=True)

    score = models.FloatField(default=0)  # ⬅️ این‌و اضافه کن

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
