from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    """ Вывод постов"""
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_posts'] = "Завтра будут новости!"
        return context


class NewsList(ListView):
    """Вывод новостей"""
    queryset = Post.objects.filter(type='NS')
    template_name = 'news.html'
    context_object_name = 'NEWS'



class ArticleList(ListView):
    """Вывод статьи"""
    template_name = 'articles.html'
    context_object_name = 'ARTS'
    queryset = Post.objects.filter(type = 'AT')


class PostDetail(DetailView):
    """Вывод отдельных постов"""
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
