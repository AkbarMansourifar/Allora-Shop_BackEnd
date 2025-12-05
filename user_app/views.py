from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Q

from auth_app.auth_utils import verify_access_token
from .models import Ban

User = get_user_model()


def get_user_from_cookie(request):
    """
    معادل authUser در فرانت: یوزر رو از روی کوکی token برمی‌گردونه (یا None)
    """
    token = request.COOKIES.get("token")
    if not token:
        return None

    payload = verify_access_token(token)
    if not payload:
        return None

    email = payload.get("email")
    if not email:
        return None

    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


from django.db import IntegrityError
from django.db.models import Q

class UserUpdateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = get_user_from_cookie(request)
        if not user:
            return Response(
                {"message": "Unauthorized: user not found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        name = request.data.get("name")
        email = request.data.get("email")
        phone = request.data.get("phone")

        if not all([name, email, phone]):
            return Response(
                {"message": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ چک کنیم ایمیل یا موبایل قبلاً برای کس دیگه نباشه
        exists = User.objects.filter(
            Q(email=email) | Q(phone=phone)
        ).exclude(id=user.id).exists()
        if exists:
            return Response(
                {"message": "email or phone already exists"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        # حالا با خیال راحت آپدیت می‌کنیم
        user.name = name
        user.email = email
        user.phone = phone
        try:
            user.save(update_fields=["name", "email", "phone"])
        except IntegrityError:
            # اگر بازم به هر دلیل constraint خطا داد
            return Response(
                {"message": "email or phone must be unique"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return Response(
            {"message": "User updated successfully :))"},
            status=status.HTTP_200_OK,
        )

class BanUserView(APIView):
    """
    معادل:
    src/app/api/user/ban/route.ts → POST
    فقط email و phone رو می‌گیره و Ban رکورد می‌سازه
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        phone = request.data.get("phone")

        if not email or not phone:
            return Response(
                {"message": "Email and phone are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Ban.objects.create(email=email, phone=phone)

        return Response(
            {"message": "User banned successfully"},
            status=status.HTTP_200_OK,
        )


class ToggleUserRoleView(APIView):
    """
    معادل:
    src/app/api/user/role/route.ts → PUT
    role کاربر رو بین USER و ADMIN عوض می‌کنه
    """

    permission_classes = [permissions.AllowAny]

    def put(self, request):
        user_id = request.data.get("id")
        if not user_id:
            return Response(
                {"message": "User ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        new_role = "ADMIN" if user.role == "USER" else "USER"
        user.role = new_role
        user.is_staff = new_role == "ADMIN"
        user.is_superuser = new_role == "ADMIN"
        user.save(update_fields=["role", "is_staff", "is_superuser"])

        return Response(
            {
                "message": f"User role updated to {new_role}",
                "newRole": new_role,
            },
            status=status.HTTP_200_OK,
        )
