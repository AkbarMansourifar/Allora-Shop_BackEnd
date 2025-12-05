from django.urls import path
from .views import WishlistAddView, WishlistRemoveView

urlpatterns = [
    path("", WishlistAddView.as_view(), name="wishlist-add"),
    path("<int:pk>/", WishlistRemoveView.as_view(), name="wishlist-remove"),
]
