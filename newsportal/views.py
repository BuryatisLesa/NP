from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    """ Вывод постов"""
    model = Post
    ordering = 'title'
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['time_now'] = datetime.utcnow()
        contex['next_posts'] = "Завтра будут новости!"
        return contex


class PostDetail(DetailView):
    """Вывод отдельных постов"""
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
