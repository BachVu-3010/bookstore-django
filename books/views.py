from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Review
from .serializers import BookSerializer, BookReviewSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

# Explicit implementation of list and individual endpoints


class BookList(APIView):

    books_per_page = 4

    """
        View to list all books in the database
    """

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        query = request.query_params.get("keyword")

        if (not query):
            query = ""
        all_books = Book.objects.all()

        filtered_books = Book.objects.filter(
            title__icontains=query).order_by("id")

        rendered_books = filtered_books

        page = request.query_params.get('page')
        paginator = Paginator(rendered_books, self.books_per_page)

        try:
            books_paginated = paginator.page(page)
        except PageNotAnInteger:
            books_paginated = paginator.page(1)
        except EmptyPage:
            books_paginated = paginator.page(paginator.num_pages)

        # When visit the homepage (no query yet)
        if (page == None):
            page = 1

        serializer = BookSerializer(books_paginated, many=True)
        return Response({'books': serializer.data, 'pages': paginator.num_pages, 'page': page})


class BookDetail(APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        # serializer = BookSerializer(book, many=False)
        serializer = BookReviewSerializer(book, many=False)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = request.data

        book = Book.objects.create(
            title=data["title"],
            description=data["description"],
            author_name=data["authorName"],
            publisher_name=data["publisherName"],
            published_date=data["publishedDate"],
            unit_price=data["unitPrice"],
            image=data["image"],
            numberOfItems=data["numberOfItems"],
            total_rating_value=data["totalRatingValue"],
            total_rating_count=data["totalRatingCount"]
        )

        return Response({"message": 'Book added'})


class AdminCreateBook(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        print(request.data)
        book_serializer = BookSerializer(data=request.data)
        if book_serializer.is_valid():
            book_serializer.save()
            return Response(book_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookReview(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = request.user
        book = Book.objects.get(id=pk)
        data = request.data

        # 1 - Review already exists
        alreadyExists = book.review_set.filter(user=user).exists()
        if alreadyExists:
            content = {'detail': 'Book is already reviewed by this user'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 2 - No Rating or 0
        elif data['rating'] == 0:
            content = {'detail': 'Please select a rating'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 3 - Create review
        else:
            review = Review.objects.create(
                user=user,
                book=book,
                name=user.fullname,
                rating=int(data['rating']),
                comment=data['comment'],
            )

            reviews = book.review_set.all()
            book.total_rating_count = len(reviews)

            total = 0.0
            for review in reviews:
                total += review.rating
      
            book.total_rating_value = total / len(reviews)
            book.save()

            return Response({"message": 'Review Added'})

    def get(self, request, pk):
        book = Book.objects.get(id=pk)
        reviews = book.review_set.all()
        serializer = BookReviewSerializer(reviews, many=True)
        return Response(serializer.data)
