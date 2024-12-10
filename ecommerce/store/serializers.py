from rest_framework import serializers
from .models import Item, Cart, Order, OrderItem, DiscountCode

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['item_id', 'name', 'price', 'description']

class CartSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = Cart
        fields = ['user_id', 'item', 'quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['item', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'total_amount', 'discount_amount', 'discount_code', 'order_items']

class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['code', 'is_valid', 'discount_percentage']
