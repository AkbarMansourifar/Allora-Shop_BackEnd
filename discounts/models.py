from django.db import models
from django.utils import timezone

class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    uses = models.PositiveIntegerField(default=0)
    # اسم فیلد رو مثل فرانت camelCase می‌ذاریم که JSON هم "maxUse" باشه
    maxUse = models.PositiveIntegerField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} ({self.uses}/{self.maxUse})"
