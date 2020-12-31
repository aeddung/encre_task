from rest_framework import serializers
from allauth.account.adapter import get_adapter
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_auth.registration.serializers import RegisterSerializer

from .models import *

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=False, max_length=50)
    introduction = serializers.CharField(required=False, max_length=200)
    profile_image = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        data_dict['introduction'] = self.validated_data.get('introduction', '')
        data_dict['profile_image'] = self.validated_data.get('profile_image', '')

        return data_dict

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'introduction', 'profile_image')

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
        
class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True) # 유저 정보가 자동으로 전달되게끔 -> 유저 모델의 모든 필드 내용 표시
    # author = serializers.StringRelatedField() -> 유저 이름만 표시

    class Meta:
        model = Comment
        fields = ('id', 'character', 'parent', 'comment', 'author', 'reply')

    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True) # instance.reply를 통해 자식 댓글 불러오기 -> self.__class__를 통한 직렬화
        serializer.bind('', self) # 직렬화된 자식을 부모에게 연결
        return serializer.data
        

class CharacterOnlySerializer(serializers.ModelSerializer):
    parent_comments = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = ('id', 'game', 'name', 'skill', 'body', 'imgurl', 'parent_comments')

    def get_parent_comments(self, obj):
        parent_comments = obj.comments.filter(parent=None) # 최초 댓글 가져오기
        serializer = CommentSerializer(parent_comments, many=True)
        return serializer.data

class CharacterSerializer(serializers.ModelSerializer):
    total_comments = serializers.SerializerMethodField()
    parent_comments = serializers.SerializerMethodField()
    gamename = serializers.ReadOnlyField(source='game.title')

    class Meta:
        model = Character
        # game이란 input 요소가 입력되어야 함
        fields = ('id', 'game', 'gamename', 'name', 'skill', 'body', 'imgurl', 'total_comments', 'parent_comments') # 기본적인 필드부터 앞에 위치 

    def get_total_comments(self, instance):
        return instance.comments.count()

    def get_parent_comments(self, obj):
        parent_comments = obj.comments.filter(parent=None)
        serializer = CommentSerializer(parent_comments, many=True)
        return serializer.data