from django.urls import path
from .views import MyTokenObtainPairView, registerUser, getUserProfile, updateUserProfile, EmailVerify
from .views import PasswordReset, PasswordResetVerify, PasswordResetVerified
from .views import getUserReviews
from .views import getUsers, getUserById, deleteUser, updateUser

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('register/', registerUser, name='register'),
    path('register/verify/', EmailVerify.as_view(),
         name='email-verify'),
    path('password/reset/', PasswordReset.as_view(),
         name='password-reset'),
    path('password/reset/verify/', PasswordResetVerify.as_view(),
         name='password-reset-verify'),
    path('password/reset/verified/', PasswordResetVerified.as_view(),
         name='password-reset-verified'),
    path('profile/', getUserProfile, name="users-profile"),
    path('profile/update/', updateUserProfile, name='user-profile-update'),
    path('reviews/', getUserReviews, name="users-reviews"),
    path("", getUsers, name="getAllUsers"),
    path("<str:pk>/", getUserById, name="getUserById"),
    path("delete/<str:pk>/", deleteUser, name="deleteUser"),
    path("update/<str:pk>/", updateUser, name="updateUser")]
