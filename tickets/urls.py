from django.urls import path
from .views import TicketCreateView, TicketAnswerView

urlpatterns = [
    path("", TicketCreateView.as_view(), name="ticket-create"),        # /api/tickets/
    path("answer", TicketAnswerView.as_view(), name="ticket-answer-no-slash"),
    path("answer/", TicketAnswerView.as_view(), name="ticket-answer"), # /api/tickets/answer/
]
