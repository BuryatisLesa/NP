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
from django.core.paginator import Paginator

def post_list(request):
    '''метод для вывода списка постов, категорий фильтрация и пагинация их'''
    posts = Post.objects.all() # queryset модели Post, выводит все имеющие посты в БД
    categories = Category.objects.all() # queryset модели Category, выводит все имеющие категории
    filterset = PostFilter(request.GET, queryset=posts) # экземпляр класса PostFilter, получает данные для фильтрации queryset = posts
    filtered_posts = filterset.qs # queryset отфильтрованные данные
    paginator = Paginator(filtered_posts, 10) # использование встроенного класса django - Paginator, для разделение постов по странично
    page_number = request.GET.get('page') # переменная для получение номера страницы
    page_obj = paginator.get_page(page_number) # добавление в экземпляр номер страницы для вывода данных
        
    context = {
        'posts': page_obj, # вывод постов
        'list_categories': categories, # вывод списка имеющих категорий
        'filterset': filterset, # отображение фильтрации
        'page_obj': page_obj # отображение пагинации
    }
    return render(request, 'index.html', context)

def post_detail(request, slug):
    """Метод для получение и отправки данных на страничке поста"""
    post = Post.objects.get(slug=slug) # Данные поста взятые по slug
    categories_post = PostCategory.objects.filter(post=post) # Данные категорий этого поста отфильтрованные с помощью filter(post=post)
    list_categories = Category.objects.all()
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
        'POST_DETAIL': post, # вывод данных отдельного поста
        'comments' : comments, # вывод имеющих комментарий к посту
        'form': form, # передача валидности формы в БД
        'categories': categories_post, # вывод категорий под каждым постом
        'list_categories':list_categories # вывод имеющих категорий в БД
    }
    return render(request, 'post_detail.html', context)

def news_list(request):
    '''метод для вывода постов с типом NS'''
    news = Post.objects.filter(type='NS') # отфильтрованные queryset по типу NS
    categories = Category.objects.all() # queryset модели Category
    paginator = Paginator(news, 10) # пагинация
    page_number = request.GET.get('page') # получение номера страницы
    page_obj = paginator.get_page(page_number) # добавление в пагинацию номер страницы
    context = {
        'NEWS': page_obj, # вывод постов
        'list_categories': categories, # вывод списка имеющих категорий в БД
        'page_obj': page_obj # вывод пагинации
    }
    return render(request, 'news.html', context)

def article_list(request):
    '''метод для вывода постов по типу AT'''
    article = Post.objects.filter(type='AT') # отфильтрованные queryset по типу AT
    list_categories = Category.objects.all() # queryset модели Category
    paginator = Paginator(article, 10) # пагинация
    page_number = request.GET.get('page') # получение номера страницы
    page_obj = paginator.get_page(page_number) # добавление номера страницы в пагинацию для отфильтровки данных
    context = {
        'ARTS': page_obj, # вывод постов по типу AT
        'page_obj':page_obj, # вывод пагинации
        'list_categories':list_categories # вывод имеющих категорий в БД
    }
    return render(request, 'articles.html', context)

class PostCreate(LoginRequiredMixin,CreateView): # в будущем возможно надо будет переписать для более гибкого функционала используя функции
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


class PostUpdate(LoginRequiredMixin,UpdateView): # в будущем возможно надо будет переписать для более гибкого функционала используя функции
    """Редактирование постов"""
    raise_exception = True
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostDelete(LoginRequiredMixin,DeleteView): # в будущем возможно надо будет переписать для более гибкого функционала используя функции
    """Удаление постов"""
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('HomePage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryList(ListView): # в будущем возможно надо будет переписать для более гибкого функционала используя функции
    """Вывод категорий"""
    model = Category
    template_name = 'categories/theme.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProfileList(ListView): # в будущем возможно надо будет переписать для более гибкого функционала используя функции
    '''Данные пользователя для отображение в профиле'''
    queryset = User.objects.all()
    template_name = "auth/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

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


