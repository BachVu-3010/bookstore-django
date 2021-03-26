from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from .models import CustomUser, SignupCode, PasswordResetCode
from books.models import Review, Book
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken, PasswordResetSerializer, PasswordResetVerifiedSerializer, UserReviewSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status

from datetime import date


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = CustomUser.objects.create(
            fullname=data['fullname'],
            phone=data['phone'],
            email=data['email'],
            birthday=data['birthday'],
            password=make_password(data['password']),
            is_active=False  # user needs to activate account before login
        )

        ipaddr = request.META.get('REMOTE_ADDR', '0.0.0.0')
        signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
        signup_code.send_signup_email()

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)

    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):

    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data

    user.fullname = data['fullname']
    user.phone = data['phone']
    user.email = data['email']
    user.birthday = data['birthday']

    password_check = check_password(data['password'], user.password)
    print(password_check)

    if password_check:
        # user.password = make_password(data['password'])
        user.save()
        return Response(serializer.data)
    else:

        message = {'detail': 'Password is incorrect'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


class EmailVerify(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        code = request.GET.get('code', '')
        verified = SignupCode.objects.set_user_is_verified(code)

        if verified:
            try:
                signup_code = SignupCode.objects.get(code=code)
                signup_code.delete()
            except SignupCode.DoesNotExist:
                pass
            content = {'success': 'Email address verified.'}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {'detail': 'Unable to verify user.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']

            try:
                user = CustomUser.objects.get(email=email)

                # Delete all unused password reset codes
                PasswordResetCode.objects.filter(user=user).delete()

                if user.is_active:
                    password_reset_code = \
                        PasswordResetCode.objects.create_password_reset_code(
                            user)
                    password_reset_code.send_password_reset_email()
                    content = {'email': email}
                    return Response(content, status=status.HTTP_201_CREATED)

            except get_user_model().DoesNotExist:
                pass

            # Since this is AllowAny, don't give away error.
            content = {'detail': 'Password reset not allowed.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerify(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        code = request.GET.get('code', '')

        try:
            password_reset_code = PasswordResetCode.objects.get(code=code)

            # Delete password reset code if older than expiry period
            delta = date.today() - password_reset_code.created_at.date()
            if delta.days > PasswordResetCode.objects.get_expiry_period():
                password_reset_code.delete()
                raise PasswordResetCode.DoesNotExist()

            content = {'success': 'Email address verified.'}
            return Response(content, status=status.HTTP_200_OK)
        except PasswordResetCode.DoesNotExist:
            content = {'detail': 'Unable to verify user.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerified(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetVerifiedSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data['code']
            password = serializer.data['password']

            try:
                password_reset_code = PasswordResetCode.objects.get(code=code)
                password_reset_code.user.set_password(password)
                password_reset_code.user.save()

                # Delete password reset code just used
                password_reset_code.delete()

                content = {'success': 'Password reset.'}
                return Response(content, status=status.HTTP_200_OK)
            except PasswordResetCode.DoesNotExist:
                content = {'detail': 'Unable to verify user.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserReviews(request):
    user = request.user
    reviews = user.review_set.all()
    serializer = UserReviewSerializer(reviews, many=True)
    return Response(serializer.data)

# IsAdminUser


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = CustomUser.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    deletedUser = CustomUser.objects.get(id=pk)
    deletedUser.delete()
    return Response(f"User {pk} was deleted")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
    user = CustomUser.objects.get(id=pk)
    data = request.data
    fullname = data['fullname']
    email = data['email']
    is_superuser = data['is_superuser']

    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
