from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Order_Book, ShippingAddress
from books.models import Book
from .serializers import OrderSerializer
from books.serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data
    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:

        # Create order

        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )

        # Create shipping address

        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            district=data['shippingAddress']['district'],
            city=data['shippingAddress']['city'],
            country=data['shippingAddress']['country'],
        )

        # Create order items and set order - order_book - book relationship
        for _ in orderItems:
            book = Book.objects.get(id=_['id'])
            price = book.unit_price * int(_["qty"])

            item = Order_Book.objects.create(
                book=book,
                order=order,
                qty=_['qty'],
                price=price,
                image=book.image.url

            )

        # Update stock

            book.numberOfItems -= int(item.qty)
            book.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

    user = request.user

    # try:

    #     order = Order.objects.get(id=pk)
    #     print(user, pk)
    #     if user.is_staff or order.user == user:
    #         serializer = OrderSerializer(order, many=False)
    #         return Response(serializer.data)
    #     else:
    #         return Response({'detail': 'Not authorized to view this order'},
    #                         status=status.HTTP_400_BAD_REQUEST)
    # except:
    #     return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    except:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
