from django.contrib.auth.models import Permission
from rest_framework import generics
from blog.models import Category, Post, Image, Tag
from .serializers import PostSerializer, ImageSerializer, CategorySerializer, TagSerializer
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions
from rest_framework import viewsets, status
# from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.template.defaultfilters import slugify
from django_filters.rest_framework import DjangoFilterBackend


class ActionBasedPermission(BasePermission):
    def has_permission(self, request, view):
        for permission, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return permission().has_permission(request, view)
        return True
    

class CustomPagination(PageNumberPagination):
    page = 1
    page_size = 20
    # page_size_query_param = 'page_size'
    # max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', 1)), # can not set default = self.page
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'total_page': int(self.page.paginator.num_pages),
            'results': data
        })


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
     # permission_classes = [ActionBasedPermission,]
    action_permissions = {
        IsAdminUser: ['destroy', 'create'],
    }


    def get_queryset(self):
        return Category.objects.all()


    def create(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Category Saved'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        if not pk:
            return Response({'msg': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
        category = get_object_or_404(Category, id=pk)
        category.delete()
        return Response({'msg': 'Category Deleted'}, status=status.HTTP_200_OK)


class TagView(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['category',]


    def get_queryset(self):
        return Tag.objects.all()
    

    # def list(self, request):
    #     queryset = Tag.objects.all()
    #     serializer = TagSerializer(queryset, many=True)
    #     print(serializer.data)
    #     return Response(serializer.data)

    
    def create(self, request, *args, **kwargs):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Tag Saved'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def update(self, request, pk=None):
        if not pk:
            return Response({'msg': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
        tag = Tag.object.get(id=pk)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Tag Saved'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        if not pk:
            return Response({'msg': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
        tag = get_object_or_404(Tag, id=pk)
        tag.delete()
        return Response({'msg': 'Tag Deleted'}, status=status.HTTP_200_OK)


class ImageView(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
     # permission_classes = [ActionBasedPermission,]
    action_permissions = {
        IsAdminUser: ['destroy', 'create'],
    }


    def get_queryset(self):
        return Image.objects.all()


    def create(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Image Saved'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        if not pk:
            return Response({'msg': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
        obj = get_object_or_404(Image, id=pk)
        obj.delete()
        return Response({'msg': 'Image Deleted'}, status=status.HTTP_200_OK)


class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    # permission_classes = [ActionBasedPermission,]
    pagination_class = CustomPagination
    action_permissions = {
        IsAdminUser: ['update', 'partial_update', 'destroy', 'create'],
    }
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['status',]


    def get_queryset(self):
        # if self.request.user.is_staff:
            return Post.objects.all()
        # return Post.postobjects.all()

    
    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        user = get_object_or_404(queryset, slug=pk)
        user.views += 1
        user.save()
        serializer = PostSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, **kwargs):
        data = request.data
        # data['author'] = request.user.id
        data['author'] = 1
        data['slug'] = slugify(data['title'])
        # data['category'] = int(data['category'])
        data['tag'] = int(data['tag'])
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Saved'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def update(self, request, pk=None):
        if not pk:
            return Response({'msg': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
        slug = pk
        data = request.data
        data['author'] = request.user.id
        data['author'] = 1
        data['slug'] = slugify(data['title'])
        # data['category'] = int(data['category'])
        data['tag'] = int(data['tag'])
        post = Post.objects.get(slug=slug)
        serializer = PostSerializer(post, data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, pk=None):
        if not pk:
            return Response({'msg': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
        slug = pk
        data = request.data
        data['author'] = request.user.id
        data['slug'] = slugify(data['title'])
        data['tag'] = int(data['tag'])
        post = Post.objects.get(slug=slug)
        serializer = PostSerializer(post, data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post Updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        if not pk:
            return Response({'msg': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
        slug = pk
        post = Post.objects.get(slug=slug)
        post.delete()
        return Response({'msg': 'Post Deleted'}, status=status.HTTP_200_OK)