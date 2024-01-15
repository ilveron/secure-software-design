from rest_framework import serializers

from app.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'price', 'category', 'stock')
        model = Product
