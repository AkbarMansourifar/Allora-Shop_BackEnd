from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.shortcuts import get_object_or_404

from .models import Comment
from .serializers import CommentSerializer
from products.models import Product


class CommentListCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # معادل POST در src/app/api/comments/route.ts
        username = request.data.get("username")
        email = request.data.get("email")
        body = request.data.get("body")
        score = request.data.get("score")
        product_id = request.data.get("productID")

        # Validation شبیه فرانت
        if not all([username, email, body, score, product_id]):
            return Response(
                {"message": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            score = int(score)
        except (TypeError, ValueError):
            return Response(
                {"message": "Score must be between 1 and 5"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if score < 1 or score > 5:
            return Response(
                {"message": "Score must be between 1 and 5"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # پیدا کردن محصول
        product = get_object_or_404(Product, id=product_id)

        # ساخت کامنت (مثل CommentModel.create)
        comment = Comment.objects.create(
            username=username,
            email=email,
            body=body,
            score=score,
            product=product,
        )

        # معادل push در ProductModel
        # در Django لازم نیست push جدا بزنیم، چون FK داریم
        # فقط میانگین امتیاز رو آپدیت می‌کنیم:

        comments_qs = Comment.objects.filter(product=product)
        scores = [c.score for c in comments_qs]
        if scores:
            avg_score = sum(scores) / len(scores)
            product.score = round(avg_score, 2)
            product.save(update_fields=["score"])

        serializer = CommentSerializer(comment)
        return Response(
            {"message": "Comment created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        # معادل GET در route.ts → فقط کامنت‌های isAccept: true
        comments = Comment.objects.filter(isAccept=True).order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentAcceptView(APIView):
    permission_classes = [permissions.AllowAny]  # بعداً فقط admin

    def put(self, request):
        comment_id = request.data.get("id")
        if not comment_id:
            return Response(
                {"message": "id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comment = get_object_or_404(Comment, id=comment_id)
        comment.isAccept = True
        comment.save(update_fields=["isAccept"])

        return Response(
            {"message": "Comment accepted successfully :))"},
            status=status.HTTP_200_OK,
        )


class CommentRejectView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request):
        comment_id = request.data.get("id")
        if not comment_id:
            return Response(
                {"message": "id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comment = get_object_or_404(Comment, id=comment_id)
        comment.isAccept = False
        comment.save(update_fields=["isAccept"])

        return Response(
            {"message": "Comment rejected successfully :))"},
            status=status.HTTP_200_OK,
        )
