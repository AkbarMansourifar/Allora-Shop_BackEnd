from django.contrib import admin
from .models import Discount

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("code", "uses", "maxUse", "created_at")
    search_fields = ("code",)
