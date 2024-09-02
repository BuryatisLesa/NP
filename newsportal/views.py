from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, PostCategory
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


class ArticleList(ListView):
    """Вывод статьи"""
    template_name = 'articles.html'
    context_object_name = 'ARTS'
    queryset = Post.objects.filter(type='AT')


class PostDetail(DetailView):
    """Вывод отдельных постов"""
    template_name = 'post_detail.html'
    context_object_name = 'POST_DETAIL'
    queryset = Post.objects.all()


class PostCreate(LoginRequiredMixin,CreateView):
    """Создание постов"""
    raise_exception = True
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'


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