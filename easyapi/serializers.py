from django.contrib.auth.models import User
from django.forms import widgets
from rest_framework import serializers
from easyapi.models import ForumPost


class ForumPostSerializer(serializers.HyperlinkedModelSerializer):
#    owner = serializers.Field(source='owner.username')
    owner = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail')

    class Meta:
        model = ForumPost
        fields = ('created', 'title', 'content', 'owner')
        
        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    forumPosts = serializers.HyperlinkedRelatedField(many=True, view_name='forumPost-detail')

    class Meta:
        model = User
        fields = ('url', 'username', 'forumPosts')