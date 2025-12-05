from django.urls import path
from .views import ProductListCreateView

urlpatterns = [
    path("products", ProductListCreateView.as_view(), name="products-no-slash"),
    path("products/", ProductListCreateView.as_view(), name="products"),
]
