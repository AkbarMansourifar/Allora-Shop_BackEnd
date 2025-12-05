from django.db import models
from django.utils import timezone

class Comment(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    score = models.PositiveSmallIntegerField()  # 1 تا 5

    # برای اینکه JSON خروجی مثل فرانت باشه، اسم فیلد رو isAccept می‌ذاریم
    isAccept = models.BooleanField(default=False)

    # ارتباط با محصول
    product = models.ForeignKey(
        "products.Product",
        related_name="comments",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} - {self.score}"
