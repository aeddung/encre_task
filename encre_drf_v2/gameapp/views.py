from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework import generics
# Create your views here.
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *
from .models import *
from .permissions import *

@permission_classes([AllowAny])
class Registration(generics.GenericAPIView):
    serializer_class = CustomRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        user = serializer.save(request) # request 필요 -> 오류 발생
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data
            },
                status=status.HTTP_201_CREATED,
        )

@permission_classes([AllowAny])
class Login(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user['username'] == "None":
            return Response({"message": "fail"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": user['token']
            }
        )

class Active(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class GameList(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GamePost(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = (JSONWebTokenAuthentication,)

    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GameUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = (JSONWebTokenAuthentication,)

    queryset = Game.objects.all()
    serializer_class = GameSerializer

class CharacterList(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

class CharacterDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    lookup_field = 'name' # 무조건 unique한 필드가 필요

class CharacterPost(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = (JSONWebTokenAuthentication,)

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

class CharacterUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = (JSONWebTokenAuthentication,)

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    lookup_field = 'name'

class CommentList(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentPost(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JSONWebTokenAuthentication,)

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer): # CommentSerializer 안의 author 정보 제공
        serializer.save(author=self.request.user)

class CommentUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # 2가지 조건 다 만족할 경우만!
    authentication_classes = (JSONWebTokenAuthentication,)

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
"""
class CommentOnlyList(generics.CreateAPIView):
    permission_classes = [AllowAny]

    queryset = Character.objects.all()
    serializer_class = CharacterOnlySerializer
"""
