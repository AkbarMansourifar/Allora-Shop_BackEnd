from django.shortcuts import render

# Create your views here.
# auth_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model, authenticate
from .serializers import RegisterSerializer, UserSafeSerializer
from .auth_utils import generate_access_token, generate_refresh_token, verify_access_token
from django.db import models

User = get_user_model()

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # check existence: name or email or phone
        data = serializer.validated_data
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")

        exists = User.objects.filter(models.Q(email=email) | models.Q(name=name) | models.Q(phone=phone)).exists()
        if exists:
            return Response({"message": "username or email or phone exist already!!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # create user
        user = serializer.save()
        # if first user => admin
        if User.objects.count() == 1:
            user.role = "ADMIN"
            user.is_staff = True
            user.is_superuser = True
            user.save(update_fields=["role", "is_staff", "is_superuser"])

        # generate access token and set cookie
        access_token = generate_access_token({"email": user.email})
        # Optionally generate refresh token and save to DB
        refresh_token = generate_refresh_token({"email": user.email})
        user.refresh_token = refresh_token
        user.save(update_fields=["refresh_token"])

        resp = Response({"message": "User signed up successfully"}, status=status.HTTP_201_CREATED)
        # set cookie - HttpOnly
        resp.set_cookie(
            key="token",
            value=access_token,
            httponly=True,
            samesite="Lax",
            path="/",
            # secure=True in production (HTTPS)
        )
        return resp

class SigninView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"message": "emailError or passwordError"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "User Not found"}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"message": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)

        access_token = generate_access_token({"email": user.email})
        refresh_token = generate_refresh_token({"email": user.email})
        user.refresh_token = refresh_token
        user.save(update_fields=["refresh_token"])

        resp = Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)
        resp.set_cookie(
            key="token",
            value=access_token,
            httponly=True,
            samesite="Lax",
            path="/",
            # secure=True in production
        )
        return resp

class SignoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        resp = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        # Delete cookie by setting empty value and expiry in past
        resp.delete_cookie("token", path="/")
        return resp

class MeView(APIView):
    permission_classes = [permissions.AllowAny]  # مثل فرانت، خودمون 401 می‌دیم

    def get(self, request):
        token = request.COOKIES.get("token")
        if not token:
            # دقیقاً مثل فرانت وقتی کوکی نیست
            return Response(
                {"data": None, "message": "No access!!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        payload = verify_access_token(token)
        if not payload:
            # فرانت در این حالت فقط null برمی‌گردونه با status 200
            return Response(None, status=status.HTTP_200_OK)

        email = payload.get("email")
        if not email:
            return Response(None, status=status.HTTP_200_OK)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # مثل زمانی که findOne برمی‌گرده null
            return Response(None, status=status.HTTP_200_OK)

        serializer = UserSafeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
