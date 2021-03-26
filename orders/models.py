from django.db import models

from users.models import CustomUser
from books.models import Book


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    taxPrice = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    paymentMethod = models.CharField(max_length=200)
    # time at creation vs time at update
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id}"


class Order_Book(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    image = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=2)

    def __str__(self):
        return f"order&book"


class ShippingAddress(models.Model):

    id = models.AutoField(primary_key=True, editable=False)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, blank=True)
    address = models.CharField(max_length=200, blank=False)
    district = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    # shippingPrice=models.DecimalField(
    #     max_digits = 5, decimal_places = 2, blank = True)

    def __str__(self):
        return str(self.address)
