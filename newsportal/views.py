from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm, CommentForm
from .models import Post, Category, PostCategory, Comment, User, Subscription
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.translation import gettext as _ # импортируем функцию для перевода
from django.views import View
import pytz
from django.utils import timezone


class PostList(View):
    def get(self, request):
        '''метод для вывода списка постов, категорий фильтр ация и пагинация их'''
        # queryset модели Post, выводит все имеющие посты в БД
        posts = Post.objects.all().order_by('-date')
        filterset = PostFilter(request.GET, queryset=posts)
        # queryset отфильтрованные данные
        filtered_posts = filterset.qs
        # использование встроенного класса django
        #  - Paginator, для разделение постов по странично
        paginator = Paginator(filtered_posts, 12)
        # переменная для получение номера страницы
        page_number = request.GET.get('page')
        # добавление в экземпляр номер страницы для вывода данных
        page_obj = paginator.get_page(page_number)
        # queryset модели Category, выводит все имеющие категории   
        categories = Category.objects.all()
        context = {
            'posts': page_obj,  # вывод постов
            'list_categories': categories,
            'filterset': filterset,  # отображение фильтрации
            'page_obj': page_obj,  # отображение пагинации
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones  #  добавляем в контекст все доступные часовые пояса
            }
        return render(request, 'index.html', context)
        
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('HomePage')


def post_detail(request, slug, pk):
    """Метод для получение и отправки данных на страничке поста"""
    # кэширование
    obj = cache.get(f'post-{pk}', None)
    if not obj:
        # если объекта нет в кэше, то получаем его и записываем в кэш
        obj = get_object_or_404(Post, pk=pk, slug=slug)
        cache.set(f'post-{pk}', obj)
    # Данные категорий этого поста отфильтрованные с помощью filter(post=post)
    categories_post = PostCategory.objects.filter(post=obj)
    list_categories = Category.objects.all()

    if request.method == 'POST':  # Отправление данных на сервер
        form = CommentForm(request.POST)  # Сохранение данных в переменной
        if form.is_valid():  # Проверка данных
            comment = form.save(commit=False)  # Сохранение
            # Передача данных об авторе комментария
            comment.user = request.user
            comment.post = obj  # Передача содержание комментарий
            comment.save()  # Сохранение данных в БД
            # Перенаправление на url=PostDetail
            return redirect('PostDetail', pk=pk, slug=slug)
    else:
        form = CommentForm()  # Отправка пустой формы
    comments = Comment.objects.filter(post=obj)  # Фильтрация данных по посту
    context = {
        'POST_DETAIL': obj,  # вывод данных отдельного поста
        'comments': comments,  # вывод имеющих комментарий к посту
        'form': form,  # передача валидности формы в БД
        'categories': categories_post,  # вывод категорий под каждым постом
        'list_categories': list_categories  # вывод имеющих категорий в БД
    }
    return render(request, 'post_detail.html', context)


# @cache_page(60*5)  # кэширование новостей на 5 мин на news.html
def news_list(request):
    '''метод для вывода постов с типом NS'''
    # отфильтрованные queryset по типу NS
    news = Post.objects.filter(type='NS').order_by('-date')
    filterset = PostFilter(request.GET, queryset=news)
    # использование встроенного класса django
    # queryset отфильтрованные данные
    filtered_news = filterset.qs
    categories = Category.objects.all()  # queryset модели Category
    paginator = Paginator(filtered_news, 12)  # пагинация
    page_number = request.GET.get('page')  # получение номера страницы
    # добавление в пагинацию номер страницы
    page_obj = paginator.get_page(page_number)
    context = {
        'NEWS': page_obj,  # вывод постов
        'list_categories': categories,  # вывод списка имеющих категорий в БД
        'page_obj': page_obj,  # вывод пагинации
        'filterset': filterset,
    }
    return render(request, 'news.html', context)


# @cache_page(60*5)  # кэширование новостей на 5 мин на articles.html
def article_list(request):
    '''метод для вывода постов по типу AT'''
    # отфильтрованные queryset по типу AT
    article = Post.objects.filter(type='AT').order_by('-date')
    filterset = PostFilter(request.GET, queryset=article)
    # queryset отфильтрованные данные
    filtered_art = filterset.qs
    list_categories = Category.objects.all()  # queryset модели Category
    paginator = Paginator(filtered_art, 10)  # пагинация
    page_number = request.GET.get('page')  # получение номера страницы
    # добавление номера страницы в пагинацию для отфильтровки данных
    page_obj = paginator.get_page(page_number)
    context = {
        'filterset': filterset,
        'ARTS': page_obj,  # вывод постов по типу AT
        'page_obj': page_obj,  # вывод пагинации
        'list_categories': list_categories  # вывод имеющих категорий в БД
    }
    return render(request, 'articles.html', context)


class PostCreate(LoginRequiredMixin, CreateView):
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


class PostUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование постов"""
    raise_exception = True
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostDelete(LoginRequiredMixin, DeleteView):
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
    template_name = 'categories.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProfileList(ListView):
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
    '''Метод для подписание на определенные категории,
      а также удаление подписки на категории'''
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')
        if action == 'subscribe':
            # создается запись в БД при нажатие на кнопку
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            # удаляется запись при нажатие кнопки из БД
            Subscription.objects.filter(
                user=request.user, category=category).delete()
    categories_with_subscriprions = Category.objects.annotate(
        user_subscribed=Exists(Subscription.objects.filter(
            user=request.user, category=OuterRef('pk'),))).order_by('name')
    return render(request, 'subscriptions.html',
                  {'categories': categories_with_subscriprions})


def view_list_posts_in_category(request, slug, pk):
    category = Category.objects.get(slug=slug, pk=pk)
    category_posts = Post.objects.filter(category=category)
    list_categories = Category.objects.all()  # queryset модели Category
    context = {
        'filtered_posts_category': category_posts,
        'category': category,
        'list_categories': list_categories,
    }
    return render(request, 'list_posts_in_category.html', context)


class CategoryDetail(View):
    def get(self, request, pk, slug):
        list_categories = Category.objects.all()
        category = Category.objects.get(pk=pk, slug=slug)
        context = {'category_detail': category,
                   'list_categories': list_categories}
        return render(request, 'category_detail.html', context)
