# serializers.py
from rest_framework import serializers
from .models import Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pseudo']

class CommentSerializer(serializers.ModelSerializer):
    pseudo_username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id','pseudo_id','pseudo_username', 'text', 'created_at', 'likes', 'dislikes', 'parent_comment']

    def get_pseudo_username(self, obj):
        return obj.pseudo.pseudo
