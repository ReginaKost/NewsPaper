from django.shortcuts import render
from django.views.generic import ListView, DetailView  # импортируем класс получения деталей объекта
# from newapp.models import Post
from newapp.models import Post
from datetime import datetime


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'Posts'
    ordering = '-dateCreation'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow() # добавим переменную текущей даты time_now
        context['value1'] = None # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        return context

# создаём представление, в котором будут детали конкретного отдельного товара
class PostDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'news_id.html'  # название шаблона будет product.html
    context_object_name = 'Post'  # название объекта