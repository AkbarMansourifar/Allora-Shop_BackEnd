from django.urls import path
from .views import (
    CommentListCreateView,
    CommentAcceptView,
    CommentRejectView,
)

urlpatterns = [
    path("", CommentListCreateView.as_view(), name="comments-list-create"),
    path("accept", CommentAcceptView.as_view(), name="comment-accept-no-slash"),
    path("accept/", CommentAcceptView.as_view(), name="comment-accept"),
    path("reject", CommentRejectView.as_view(), name="comment-reject-no-slash"),
    path("reject/", CommentRejectView.as_view(), name="comment-reject"),
]
