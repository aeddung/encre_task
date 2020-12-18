from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from .serializers import BoardSerializer
from .models import Board
from drfapp.models import *

def login_user_email(request):
    #token = request.headers.get('Authorization')
    #data = {'token': token.split()[1]}
    data = {'token': request.auth}
    return VerifyJSONWebTokenSerializer().validate(data)['user'].email

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def board_list(request):
    if request.method == 'GET':
        board_set = Board.objects.all()
        serializer = BoardSerializer(board_set, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def board_update(request, board_id):
    board = Board.objects.get(id=board_id)

    if request.method == 'GET':
        serializer = BoardSerializer(board)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        email = login_user_email(request)
        user_id = User.objects.get(email=email).id
        board = Board.objects.get(id=board_id)

        if board.author.id == user_id:
            serializer = BoardSerializer(board, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Resopnse({"message": "Not same user"}, status=status.HTTP_401_UNAUTHORIZED)

    elif reuqest.method == 'DELETE':
        email = login_user_email(request)
        user_id = User.objects.get(email=email).id
        board = Board.objects.get(id=board_id)

        if board.author.id == user_id:
            board.delete()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        
        else:
            return Resopnse({"message": "Not same user"}, status=status.HTTP_401_UNAUTHORIZED)