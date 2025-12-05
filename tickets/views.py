from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Ticket
from .serializers import TicketSerializer
from auth_app.auth_utils import verify_access_token

User = get_user_model()


def get_user_from_cookie(request):
    """
    معادل authUser در فرانت:
    از روی کوکی token، یوزر رو برمی‌گردونه یا None
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


class TicketCreateView(APIView):
    """
    معادل src/app/api/tickets/route.ts → POST
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # سعی می‌کنیم کاربر رو از روی کوکی پیدا کنیم، ولی اجباری نیست
        user = None
        try:
            user = get_user_from_cookie(request)
        except Exception:
            user = None

        name = request.data.get("name")
        message = request.data.get("message")
        phone = request.data.get("phone")
        email = request.data.get("email")

        if not all([name, message, phone, email]):
            return Response(
                {"message": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ticket = Ticket.objects.create(
            name=name,
            message=message,
            phone=phone,
            email=email,
            user=user,
        )

        return Response(
            {"message": "Ticket saved successfully."},
            status=status.HTTP_200_OK,
        )


class TicketAnswerView(APIView):
    """
    معادل src/app/api/tickets/answer/route.ts → POST
    فقط ادمین اجازه داره
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        body = request.data
        message = body.get("message")
        ticket_id = body.get("ticketID")

        if not message:
            return Response(
                {"message": "Message field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # معادل authUser + role === "ADMIN"
        admin = get_user_from_cookie(request)

        if not admin or admin.role != "ADMIN":
            return Response(
                {"message": "Not authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # آپدیت تیکت اصلی: hasAnswer = true
        main_ticket = Ticket.objects.filter(id=ticket_id, isAnswer=False).first()
        if not main_ticket:
            return Response(
                {"message": "Ticket not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        main_ticket.hasAnswer = True
        main_ticket.save(update_fields=["hasAnswer"])

        # ساخت رکورد پاسخ
        Ticket.objects.create(
            name=admin.name,
            message=message,
            phone=admin.phone,
            email=admin.email,
            user=admin,
            hasAnswer=False,
            isAnswer=True,
            mainTicket=main_ticket,
        )

        return Response(
            {"message": "Answer saved successfully"},
            status=status.HTTP_200_OK,
        )
