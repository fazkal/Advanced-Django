# from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView  # ,RedirectView
from django.views.generic import (
    ListView,
    # FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.detail import DetailView
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "ali"
        context["posts"] = Post.objects.all()
        return context


"""class RedirectToMaktab(RedirectView):
    url = "https://maktabkhooneh.com"

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        return super().get_redirect_url(*args, **kwargs)"""


class PostList(ListView):
    # model=Post
    queryset = Post.objects.all()
    context_object_name = "posts"
    paginate_by = 2
    ordering = "-id"

    # def get_queryset(self):
    # posts=Post.objects.filter(status=True)
    # return posts

class PostListApiView(TemplateView):
    template_name='blog/post_list_api.html'


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


"""
class PostCreateView(FormView):
    template_name='contact.html'
    form_class=PostForm
    success_url='/blog/post/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
"""


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "status", "category", "published_date"]
    success_url = "/blog/post/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post/"


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/blog/post/"
