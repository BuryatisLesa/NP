from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, PostCategory, User, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostList(ListView):
    """ Вывод постов"""
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset) # передает запрос на фильтрацию данных queryset
        return self.filterset.qs # возвращает отфильтрованные данные queryset в шаблон index.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['users'] = User.objects.all()
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


class PostDetail(DetailView):
    """Вывод отдельных постов"""
    template_name = 'post_detail.html'
    context_object_name = 'POST_DETAIL'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # переопределяем метод
        context['comments'] = Comment.objects.all()
        return context


class PostCreate(LoginRequiredMixin,CreateView):
    """Создание постов"""
    # permission_required = ('newsportal.add_post')
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
    # permission_required = ('newsportal.change_post')
    raise_exception = True
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin,DeleteView):
    """Удаление постов"""
    # permission_required = ('newsportal.delete_post')
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('HomePage')


class CategoryList(ListView):
    """Вывод категорий"""
    model = Category
    template_name = 'categories/theme.html'
    context_object_name = 'categories'


class ProfileList(LoginRequiredMixin,ListView):
    '''Профиль пользователя'''
    raise_exception = True
    template_name = 'auth/profile.html'
    context_object_name = 'users'
    queryset = User.objects.all()


