from django.urls import path
from orders.views import getMyOrders, getOrders, addOrderItems, getOrderById


urlpatterns = [

    path('', getOrders, name='getOrders'),
    path('create/', addOrderItems, name='addOrderItems'),
    path('myorders/', getMyOrders, name='getMyOrders'),
    path('<int:pk>/', getOrderById, name='getOrderById'),
]
