from rest_framework import serializers
from .models import Book, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('id', 'created_date', 'updated_date',)


class BookReviewSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
