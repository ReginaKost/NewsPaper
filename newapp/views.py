from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from newapp.models import Post, Category
from datetime import datetime
from django.urls import reverse_lazy
from .forms import AddPostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import PostFilter
from django.views.generic import TemplateView

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string



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




class NewsCategoryView(ListView):
    model = Post
    template_name = 'category.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты
    ordering = ['-time_creation']
    paginate_by = 15
    #form_class = NewsForm
    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        queryset = News.objects.filter(category=c)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category  = Category.objects.get(id=self.id)
        subscribed = category.subscribers.filter(email=user.email)
        if not subscribed:
            context['sub'] = True
        else:
            context['sub'] = False
        context['category'] = category
        return context

def subscribe_to_category(request,pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user.id)
        email = user.email
        html_content = render_to_string (
            'mailing/subscribed.html',
            {
                'categories': category,
                'user' : user,
            },
        )
        msg = EmailMultiAlternatives(
            subject=f'Sign up confirmation - {category}',
            body='',
            from_email='2779605@gmail.com',
            to=[email,], # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html") # добавляем html
        try:
            msg.send() # отсылаем
        except Exception as e:
            print(e)
        return redirect('index')
    return redirect(request.Meta.get('HTTP_REFERER'))

def unsubscribe_to_category(request,pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user.id)
    return redirect('index')


