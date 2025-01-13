from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Post
# Create your views here.

class IndexView(TemplateView):
    template_name='index.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['name']='ali'
        context['posts']=Post.objects.all()
        return context