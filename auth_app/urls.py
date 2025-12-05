# auth_app/urls.py
from django.urls import path
from .views import SignupView, SigninView, SignoutView, MeView

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup-no-slash"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin", SigninView.as_view(), name="signin-no-slash"),
    path("signin/", SigninView.as_view(), name="signin"),
    path("signout", SignoutView.as_view(), name="signout-no-slash"),
    path("signout/", SignoutView.as_view(), name="signout"),
    path("me", MeView.as_view(), name="me-no-slash"),
    path("me/", MeView.as_view(), name="me"),
]
