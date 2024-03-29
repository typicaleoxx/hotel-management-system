from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from .models import RoomType, Room, User
from .serializers import (
    RoomTypeSerializer,
    RoomSerializer,
    UserSerializer,
    GroupSerializer,
)
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import Group
from rest_framework import filters


class GroupView(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]


# TODO make logic for login
# Create your views here.
# everymodel ko CRUD operation  garna
# views ma define garne
# restframework ko class banaunu parcha
# sothat API class huncha, ani url ma user le request gareko anusar pass garna milcha
# WE USE DJANGO REST FRAMEWORK
# api ma hune everything all the logic is inside rest framework
# so we use djangorest framework
# to use it we must also define in settings


class RoomTypeView(ModelViewSet):
    # modelviewset lai inherit garera normal class lai we made api view class
    # crud operation ko lagi afai le define nai garna pardaina everything is inside rest framework
    # it has two requirement i.e query_set and serializer_class
    # queryset=   #kun model ma crud garne ho define garne yeta
    # serializer_class=#component where object lai json and json lai object ma convert garna milcha
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

class RoomView(GenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_fields=["type"]
    search_fields = ['name',]

    def get(self, request):
        room_objs = Room.objects.all()
        filter_objs=self.filter_queryset(room_objs)
        serializer = RoomSerializer(filter_objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# sabai data list garna ni we do get request ani specific data ko lagi ni get


# tesaile duita get banayera hunna, overwrite huncha
# thats why generic API view ma kaam garda
# we make different view for edit view and delete
class RoomEditView(GenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, pk):
        try:
            room_obj = Room.objects.get(id=pk)
        except:
            return Response("Data not found!")
        serializer = RoomSerializer(room_obj)
        return Response(serializer.data)

    def put(self, request, pk):
        room_obj = Room.objects.get(id=pk)
        serializer = RoomSerializer(room_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        try:
            room_obj = Room.objects.get(id=pk)
        except:
            return Response("Data not found")
        room_obj.delete()
        return Response("Data has been successfully deleted")


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get("password")
            hash_password = make_password("password")
            a = serializer.save()
            a.password = hash_password
            a.save()
            return Response("User Created !")
        else:
            return Response(serializer.errors)

    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)

        if user == None:
            return Response("Invalid credentials !")
        else:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(token.key)
