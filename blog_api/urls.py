from .views import PostView, ImageView, CategoryView, TagView
# from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'blog_api'

router = DefaultRouter()
router.register('blog', PostView, basename='post')
router.register('image', ImageView, basename='image')
router.register('category', CategoryView, basename='category')
router.register('tag', TagView, basename='tag')
urlpatterns = router.urls

# urlpatterns += [
#     path('<int:pk>/', PostDetail.as_view(), name='detailcreate'),
    # path('drafts/', DraftList.as_view(), name='list'),
# ]
