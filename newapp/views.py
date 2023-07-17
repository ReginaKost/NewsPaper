from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from newapp.models import Post
from datetime import datetime
from django.urls import reverse_lazy
from .forms import AddPostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import PostFilter
from django.views.generic import TemplateView




class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    ordering = '-dateCreation'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'news_id.html'
    context_object_name = 'post'

class PostCreate(CreateView):
    template_name = 'post_create.html'
    form_class = AddPostForm


class PostUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = AddPostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'prodected_page.html'

class PostDelete(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news')



