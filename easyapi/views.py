from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from easyapi.models import ForumPost
from easyapi.serializers import ForumPostSerializer, UserSerializer
#from snippets import permissions as snippetsPermissions


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'forumPosts': reverse('forumPost-list', request=request, format=format)
    })


class ForumPostList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#    permission_classes = (snippetsPermissions.IsOwner,)

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
        
        
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
