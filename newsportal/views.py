from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm, CommentForm
from .models import Post, Category, PostCategory, Author, Comment, User, Subscription
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef


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
        context['categories'] = Category.objects.all()
        return context


class NewsList(ListView):
    """Вывод новостей"""
    queryset = Post.objects.filter(type='NS')
    template_name = 'news.html'
    context_object_name = 'NEWS'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ArticleList(ListView):
    """Вывод статьи"""
    template_name = 'articles.html'
    context_object_name = 'ARTS'
    queryset = Post.objects.filter(type='AT')
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


# class PostDetail(DetailView, CreateView):
#     """Вывод отдельных постов"""
#     template_name = 'post_detail.html'
#     context_object_name = 'POST_DETAIL'
#     queryset = Post.objects.all()
#     form_class = CommentForm # форма для создание комментарий под постом

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['comments'] = Comment.objects.filter(post=self.get_object())
#         context['categories'] = Category.objects.all()
#         return context

#     def form_valid(self, form):
#         # Валидация формы комментария
#         comment = form.save(commit=False)
#         comment.user = self.request.user
#         comment.post = self.get_object()
#         comment.save()
#         return super().form_valid(form)

#     def get_success_url(self):
#         # Перенаправление после создание комментария на страничку поста
#         return reverse('PostDetail', kwargs={'pk': self.get_object().pk})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostUpdate(LoginRequiredMixin,UpdateView):
    """Редактирование постов"""
    raise_exception = True
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostDelete(LoginRequiredMixin,DeleteView):
    """Удаление постов"""
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('HomePage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryList(ListView):
    """Вывод категорий"""
    model = Category
    template_name = 'categories/theme.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProfileList(ListView):
    queryset = User.objects.all()
    template_name = "auth/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CategoryDetail(DetailView):
    template_name = 'category_detail.html'
    context_object_name = 'CATEGORY_DETAIL'
    queryset = Category.objects.all()



@login_required
@csrf_protect
def subscriptions(request):
    '''Метод для подписание на определенные категории, а также удаление подписки на категории'''
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')
        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action  == 'unsubscribe':
            Subscription.objects.filter(user=request.user, category=category).delete()
    categories_with_subscriprions = Category.objects.annotate(user_subscribed = Exists(Subscription.objects.filter(user=request.user, category = OuterRef('pk'),))).order_by('name')
    return render(request, 'subscriptions.html', {'categories':categories_with_subscriprions})

def post_detail(request, slug):
    """Метод для получение и отправки данных на страничке поста"""
    post = Post.objects.get(slug=slug) # Данные поста взятые по slug
    categories = PostCategory.objects.filter(post=post) # Данные категорий этого поста отфильтрованные с помощью filter(post=post)
    if request.method == 'POST': # Отправление данных на сервер
        form = CommentForm(request.POST) # Сохранение данных в переменной
        if form.is_valid(): # Проверка данных
            comment = form.save(commit=False) # Сохранение
            comment.user = request.user # Передача данных об авторе комментария
            comment.post = post # Передача содержание комментарий
            comment.save() # Сохранение данных в БД
            return redirect('PostDetail', slug=slug) # Перенаправление на url=PostDetail
    else:
        form = CommentForm() # Отправка пустой формы
    comments = Comment.objects.filter(post=post) # Фильтрация данных по посту
    context = {
        'POST_DETAIL': post,
        'comments' : comments,
        'form':form,
        'categories': categories
    }
    return render(request, 'post_detail.html', context)
