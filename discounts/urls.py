from django.urls import path
from .views import DiscountUseView

urlpatterns = [
    path("use", DiscountUseView.as_view(), name="discount-use-no-slash"),
    path("use/", DiscountUseView.as_view(), name="discount-use"),
]
