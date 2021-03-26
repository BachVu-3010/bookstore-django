from django.db import models

from users.models import CustomUser


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author_name = models.CharField(max_length=255)
    publisher_name = models.CharField(max_length=255)
    published_date = models.DateField(
        auto_now=False, auto_now_add=False)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='', blank=True, null=True)
    total_rating_value = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, blank=True, default=0.0)
    total_rating_count = models.IntegerField(null=True, blank=True, default=0)
    numberOfItems = models.IntegerField()
    # time at creation vs time at update
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class Review(models.Model):
    # to model the one to many relationship use ForeignKey
    # ForeignKey, ManyToManyField and OneToOneField
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)
