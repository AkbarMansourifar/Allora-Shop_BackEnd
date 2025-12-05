import os
import json
import time

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            form = request.data

            name = form.get("name")
            price_raw = form.get("price")
            description = form.get("description")
            category = form.get("category")
            stock_raw = form.get("stock")
            discount_raw = form.get("discount")
            variants_raw = form.get("variants")

            # Cast values
            try:
                price = float(price_raw)
            except:
                price = None

            try:
                stock = int(stock_raw)
            except:
                stock = None

            try:
                discount = int(discount_raw)
            except:
                discount = None

            # Validation (matching Next.js)
            if not name or len(name.strip()) < 3:
                return Response({"message": "Invalid product name. It must be at least 3 characters long."}, status=400)

            if not price or price <= 0:
                return Response({"message": "Invalid price. It must be a positive number."}, status=400)

            if not description or len(description.strip()) < 10:
                return Response({"message": "Invalid description. It must be at least 10 characters long."}, status=400)

            if not category:
                return Response({"message": "Invalid category."}, status=400)

            if stock is None or stock < 0:
                return Response({"message": "Invalid stock value. It must be a non-negative number."}, status=400)

            if discount is None or discount < 0 or discount > 100:
                return Response({"message": "Invalid discount. It must be between 0 and 100."}, status=400)

            # Parse variants
            clean_variants = []
            if variants_raw:
                try:
                    variants = json.loads(variants_raw)
                    for v in variants:
                        cleaned = {
                            "color": {
                                "name": v.get("colorName"),
                                "hex": v.get("colorHex"),
                            },
                            "size": v.get("size"),
                            "stock": int(v["stock"]) if v.get("stock") else None,
                            "price": float(v["price"]) if v.get("price") else None,
                        }
                        if any([cleaned["color"]["name"], cleaned["color"]["hex"], cleaned["size"], cleaned["stock"], cleaned["price"]]):
                            clean_variants.append(cleaned)
                except:
                    return Response({"message": "Invalid variants format."}, status=400)

            # Handle images
            imgs = request.FILES.getlist("img")
            if not imgs:
                return Response({"message": "At least one product image is required."}, status=400)

            img_urls = []
            upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
            os.makedirs(upload_dir, exist_ok=True)

            for img in imgs:
                filename = f"{int(time.time()*1000)}-{img.name.replace(' ', '_')}"
                file_path = os.path.join(upload_dir, filename)

                with open(file_path, "wb+") as dest:
                    for chunk in img.chunks():
                        dest.write(chunk)

                img_urls.append(settings.MEDIA_URL + "uploads/" + filename)

            product = Product.objects.create(
                name=name,
                price=price,
                description=description,
                category=category,
                stock=stock,
                discount=discount,
                variants=clean_variants,
                images=img_urls
            )

            return Response({
                "message": "Product created successfully",
                "data": ProductSerializer(product).data
            }, status=201)

        except Exception as e:
            return Response({"message": str(e)}, status=500)

    def get(self, request):
        try:
            products = Product.objects.all().order_by("-created_at")
            return Response(ProductSerializer(products, many=True).data, status=200)
        except Exception as e:
            return Response({"message": str(e)}, status=500)
