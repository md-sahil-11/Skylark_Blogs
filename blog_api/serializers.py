from django.db import models
from django.db.models import fields
from django.template.defaultfilters import slugify
from rest_framework import serializers
from blog.models import Category, Post, Image, Tag
from django.conf import settings


class PostSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='tag.category.id', read_only=True)
    category_name = serializers.CharField(source='tag.category', read_only=True)
    tag_name = serializers.CharField(source='tag.name', read_only=True)
    author_name = serializers.CharField(source='author.first_name', read_only=True)

    class Meta:
        model = Post
        fields = ('tag', 'id', 'title', 'slug', 'author',
                  'excerpt', 'content', 'status', 'banner', 
                  'published', 'views', 'likes', 
                  'tag_name', 'author_name', 'category', 'category_name')


class PostSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'slug', 'banner', 
                    'excerpt', 'likes', 'views', 'author')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'id')


class TagSerializer(serializers.ModelSerializer):
    # posts = PostSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ('name', 'id', 'posts', 'category')
        read_only_fields = ('posts',)

    
class TagListSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Tag
        fields = ('name', 'id') 


class CategorySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'id', 'tags')


class UserRegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('email', 'user_name', 'first_name')
        extra_kwargs = {'password': {'write_only': True}}
