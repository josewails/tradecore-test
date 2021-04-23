import json

from rest_framework import serializers
from .models import User


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
