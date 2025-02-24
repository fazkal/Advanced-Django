# from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "api-v1"

# Generating urls via DefaultRouter
router = DefaultRouter()
router.register("post", views.PostModelViewSet, basename="post")
router.register("category", views.CategoryModelViewSet, basename="category")
urlpatterns = router.urls

# urlpatterns = [

# path('post/', views.postList,name='post-list'),
# path('post/<int:id>',views.postDetail,name='post-detail'),
# path('post/',views.PostList.as_view(),name='post-list'),
# path('post/<int:pk>',views.PostDetail.as_view(),name='post-detail'),
# ]
