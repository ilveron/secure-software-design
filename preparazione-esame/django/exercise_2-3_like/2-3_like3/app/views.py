from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.models import Product
from app.permissions import IsPostEditorOrReadOnly
from app.serializers import ProductSerializer


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostEditorOrReadOnly, IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        name_query = self.request.query_params.get("name")
        category_query = self.request.query_params.get("category")
        price_min = self.request.query_params.get("price_min")
        price_max = self.request.query_params.get("price_max")
        if name_query:
            queryset = queryset.filter(name__icontains=name_query)
        if category_query:
            queryset = queryset.filter(category__icontains=category_query)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        return queryset
