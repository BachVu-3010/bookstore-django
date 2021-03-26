from django.urls import path

from .views import BookList, BookDetail, BookReview, AdminCreateBook


urlpatterns = [
    path("", BookList.as_view()),
    path("<int:pk>/", BookDetail.as_view()),
    path("<int:pk>/reviews/", BookReview.as_view()),
    path("create/", BookDetail.as_view()),
]
