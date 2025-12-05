from django.urls import path
from .views import UserUpdateView, BanUserView, ToggleUserRoleView

urlpatterns = [
    path("", UserUpdateView.as_view(), name="user-update"),          # /api/user/
    path("ban/", BanUserView.as_view(), name="user-ban"),            # /api/user/ban/
    path("ban", BanUserView.as_view()),                              # بدون اسلش هم ساپورت
    path("role/", ToggleUserRoleView.as_view(), name="user-role"),   # /api/user/role/
    path("role", ToggleUserRoleView.as_view()),
]
