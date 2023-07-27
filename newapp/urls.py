from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, NewsCategoryView, subscribe_to_category, unsubscribe_to_category
from django.views.decorators.cache import cache_page

app_name = 'newapp'
urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name='search'),
    path('add/', PostCreate.as_view(), name='post_create'),
    path('category/<int:pk>/', NewsCategoryView.as_view(), name='categories'),
    path('subscribe/<int:pk>/', subscribe_to_category, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe_to_category, name='unsubscribe'),
    path('<int:pk>/', cache_page(60*10)),
    ]
