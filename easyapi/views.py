from django.http import Http404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.db import IntegrityError
#from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework import mixins
from rest_framework import renderers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.reverse import reverse
from rest_framework.renderers import JSONPRenderer, JSONRenderer
import json

from easyapi.models import ForumPost
from easyapi.serializers import ForumPostSerializer, UserSerializer
from easyapi import permissions as easyapiPermissions


# Display all APIs -------------------------------------------------

class ApiRoot(APIView):
    permission_classes = (permissions.IsAdminUser,)
    
    def get(self, request, format=None):
        return Response({
            'users': reverse('user-list', request=request, format=format),
            'forumPosts': reverse('forumPost-list', request=request, format=format)
        })



# User related APIs ------------------------------------------------

class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserCreate(APIView):
    @renderer_classes((JSONRenderer, JSONPRenderer))
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.create_user(request.DATA.get('username'), request.DATA.get('email'), request.DATA.get('password'))
        except IntegrityError:
            message = { 'error': 'That username already exists' }
            return HttpResponseBadRequest(json.dumps(message), mimetype='text/json')

        return HttpResponse()



# Post related APIs ------------------------------------------------

class ForumPostList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user


class ForumPostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#    permission_classes = (snippetsPermissions.IsOwner,)
    
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user



# Testing Pages ----------------------------------------------------

def UserLoginTest(request):
    return render(request, 'userLoginTest.html', { 'value': 'my value~~' })
