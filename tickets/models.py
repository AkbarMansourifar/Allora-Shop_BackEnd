from django.db import models
from django.conf import settings
from django.utils import timezone


class Ticket(models.Model):
    name = models.CharField(max_length=255)
    message = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    # ممکنه کاربر لاگین نباشه → nullable
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="tickets",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # آیا برای این تیکت پاسخی ثبت شده؟
    hasAnswer = models.BooleanField(default=False)

    # آیا خودِ این تیکت، «جواب» یه تیکت دیگه‌ست؟
    isAnswer = models.BooleanField(default=False)

    # لینک به تیکت اصلی (برای جواب‌ها)
    mainTicket = models.ForeignKey(
        "self",
        related_name="answers",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.isAnswer:
            return f"Answer to #{self.mainTicket_id} by {self.name}"
        return f"Ticket #{self.id} - {self.name}"
