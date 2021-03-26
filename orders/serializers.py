from rest_framework import serializers
from .models import Order, ShippingAddress, Order_Book
from users.serializers import UserSerializer


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Book
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_book = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_order_book(self, obj):
        items = obj.order_book_set.all()
        serializer = OrderBookSerializer(items, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(
                obj.shippingaddress, many=False).data
        except:
            address = False
        return address

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
