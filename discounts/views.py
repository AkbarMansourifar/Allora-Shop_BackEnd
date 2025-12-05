import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Discount
from .serializers import DiscountSerializer


class DiscountUseView(APIView):
    permission_classes = [permissions.AllowAny]  # فرانت هم auth خاصی نداره

    def put(self, request):
        code = request.data.get("code")
        if isinstance(code, str):
            code = code.strip()  # فاصله‌های اول و آخر

        if (
            not code
            or not isinstance(code, str)
            or not re.fullmatch(r"[a-zA-Z0-9]{3,20}", code)
        ):
            return Response(
                {
                    "message": "Invalid discount code format. Only letters and numbers (3-20 characters) are allowed."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # جستجوی بدون حساسیت به حروف بزرگ/کوچیک
        discount = Discount.objects.filter(code__iexact=code).first()

        if not discount:
            return Response(
                {"message": "Code not found !!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if discount.uses >= discount.maxUse:
            return Response(
                {"message": "Code usage limit reached"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        discount.uses += 1
        discount.save(update_fields=["uses"])

        serializer = DiscountSerializer(discount)
        # فرانت NextResponse.json(discount) با status 200 برمی‌گردونه
        return Response(serializer.data, status=status.HTTP_200_OK)
