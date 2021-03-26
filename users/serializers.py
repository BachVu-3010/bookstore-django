from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from .models import CustomUser
from books.models import Review


class UserSerializer(serializers.ModelSerializer):
    # email = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'fullname', 'phone',
                  'birthday', "is_superuser", 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class UserReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128)


class PasswordResetVerifiedSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=40)
    password = serializers.CharField(max_length=128)
