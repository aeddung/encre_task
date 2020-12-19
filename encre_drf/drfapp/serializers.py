from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from .models import User
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

# 회원가입 api
class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])

        user.save()
        return user

# 로그인 api
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password", None)
        user = authenticate(username=username, password=password)

        if user is None:
            return {'username': 'None'}
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exist'
            )
        return {
            'username': user.username,
            'token': jwt_token
        }
