from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import Wishlist
from products.models import Product
from auth_app.models import User
from auth_app.auth_utils import verify_access_token


class WishlistAddView(APIView):
    # مثل فرانت: بدون auth خاص، فقط user و product از body میاد
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_id = request.data.get("user")
        product_id = request.data.get("product")

        if not user_id or not product_id:
            return Response(
                {"message": "User and product are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, id=user_id)
        product = get_object_or_404(Product, id=product_id)

        # مثل فرانت: اگر قبلاً وجود نداشت، بساز
        wish = Wishlist.objects.filter(user=user, product=product).first()
        if not wish:
            Wishlist.objects.create(user=user, product=product)

        return Response(
            {"message": "Product added to wishlist successfully :))"},
            status=status.HTTP_201_CREATED,
        )


class WishlistRemoveView(APIView):
    # مثل فرانت: authUser از روی کوکی
    permission_classes = [permissions.AllowAny]

    def delete(self, request, pk):
        # توکن از کوکی
        token = request.COOKIES.get("token")
        if not token:
            return Response(
                {"message": "Please login first !!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        payload = verify_access_token(token)
        if not payload:
            return Response(
                {"message": "Please login first !!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        email = payload.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "Please login first !!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # حالا مثل فرانت: حذف wishlist با user + productID (که تو URL هست)
        Wishlist.objects.filter(user=user, product_id=pk).delete()

        return Response(
            {"message": "Product removed successfully :))"},
            status=status.HTTP_200_OK,
        )
