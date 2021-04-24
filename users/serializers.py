import json

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer, PasswordField
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserSignupSerializer(TokenObtainSerializer):
    email = serializers.EmailField(required=True)
    password = PasswordField(required=True)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        email, password = validated_data["email"], validated_data["password"]
        user = User(email=email)
        user.set_password(password)
        user.save()

        super().validate(dict(email=email, password=password))
        refresh = self.get_token(user)

        return dict(refresh=str(refresh), access=str(refresh.access_token))


class UserSerializer(serializers.ModelSerializer):
    geolocation = serializers.SerializerMethodField()
    signup_holiday = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "geolocation", "signup_holiday"]

    @staticmethod
    def get_geolocation(obj):
        if obj.geolocation:
            return json.loads(obj.geolocation)

        return None

    @staticmethod
    def get_signup_holiday(obj):
        if obj.signup_holiday:
            return json.loads(obj.signup_holiday)

        return None
