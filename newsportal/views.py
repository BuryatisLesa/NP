from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm, CommentForm
from .models import Post, Category, PostCategory, Author, Comment, User
from django.contrib.auth.mixins import LoginRequiredMixin


class PostList(ListView):
    """ Вывод постов"""
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsList(ListView):
    """Вывод новостей"""
    queryset = Post.objects.filter(type='NS')
    template_name = 'news.html'
    context_object_name = 'NEWS'
    paginate_by = 5


class ArticleList(ListView):
    """Вывод статьи"""
    template_name = 'articles.html'
    context_object_name = 'ARTS'
    queryset = Post.objects.filter(type='AT')
    paginate_by = 5


class PostDetail(DetailView, CreateView):
    """Вывод отдельных постов"""
    template_name = 'post_detail.html'
    context_object_name = 'POST_DETAIL'
    queryset = Post.objects.all()
    form_class = CommentForm # форма для создание комментарий под постом

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.get_object())
        return context

    def form_valid(self, form):
        # Валидация формы комментария
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = self.get_object()
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Перенаправление после создание комментария на страничку поста
        return reverse('PostDetail', kwargs={'pk': self.get_object().pk})




class PostCreate(LoginRequiredMixin,CreateView):
    """Создание постов"""
    raise_exception = True
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def form_valid(self, form):
        # Передаем текущего пользователя в метод save формы
        form.save(user=self.request.user)
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin,UpdateView):
    """Редактирование постов"""
    raise_exception = True
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin,DeleteView):
    """Удаление постов"""
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('HomePage')


class CategoryList(ListView):
    """Вывод категорий"""
    model = Category
    template_name = 'categories/theme.html'
    context_object_name = 'categories'


class ProfileList(ListView):
    queryset = User.objects.all()
    template_name = "auth/profile.html"


def getComment(self, request):
    author = request.GET['user.username']
    text = request.GET['text']
    comment = author + ' ' + text
    return render(self.request, 'showResult.html', {'comment' : comment})