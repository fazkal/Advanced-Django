from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name='blog'

urlpatterns = [
    
    #path('cbv-index/', TemplateView.as_view(template_name='index.html',extra_context={"name":"fazel"})),
    path('cbv-index', views.IndexView.as_view(),name='cbv-index'),
    path('post/',views.PostList.as_view(),name='post-list'),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name='post-detail'),
    path('go-to-maktabkhooneh/<int:pk>',views.RedirectToMaktab.as_view(),name='redirect-to-maktabkhooneh'),
]