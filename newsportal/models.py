from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify
from time import time
from django.core.cache import cache


def gen_slug(string):
    '''метод для создание слага для постов и категорий, и т.д.'''
    # функция по создание слага
    finally_slug = slugify(string, allow_unicode=False,)
    # финальный слага + время создания
    return finally_slug + '-' + str(int(time()))


class Post(models.Model):
    """Посты"""

    class Meta:
        verbose_name = 'Пост'  # мета данные ед.ч.
        verbose_name_plural = 'Посты'  # мета данные мн.ч

    NEWS = 'NS'  # переменная типа новостей
    ARTICLE = 'AT'  # переменная типа статей
    POST_TYPE_CHOICES = [(NEWS, 'Новость'),
                         (ARTICLE, 'Статья')]
    # столбец авторов
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    # столбец типа поста
    type = models.CharField(
        max_length=2, choices=POST_TYPE_CHOICES, default='NS')
    # столбец заголовка поста
    title = models.CharField(max_length=150)
    # столбец для даты создания поста
    date = models.DateTimeField(auto_now_add=True)
    # столбец содержащий контент для поста
    content = models.TextField()
    # категории поста
    category = models.ManyToManyField(
        'Category', through='PostCategory', blank=False, related_name='posts')
    # рейтинг поста
    rating = models.IntegerField(default=0)
    # картинка поста
    image = models.ImageField(
        upload_to='images/', null=True, blank=True)
    # созданный слаг для поста на основе заголовка
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        # сохранение слага в БД
        self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)
        # удаление старого ключа кэша
        cache.delete(f'post-{self.pk}')

    def delete(self, *args, **kwargs):
        # Удаление кэша перед удалением объекта
        cache.delete(f'post-{self.pk}')
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        '''абсолютная ссылка на пост при использование в проекте'''
        return reverse('PostDetail', kwargs={'slug': self.slug, 'pk': self.pk})

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:124]}...'

    def __str__(self):
        return f'{self.title}, {self.category.all()}, {self.type}'


class Author(models.Model):
    """Авторы"""

    class Meta:
        # мета данные ед.ч
        verbose_name = 'Автор'
        # мета данные мн.ч
        verbose_name_plural = 'Авторы'
    # столбец с никнеймом автора
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    # столбец для подсчёта рейтинга автора на основе его постов и комментарий
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{User.objects.get(pk=self.name.pk)}'

    def update_rating(self):
        '''обновление и суммирование рейтинга'''
        # фильтрация постов созданным автором
        posts = Post.objects.filter(author_id=self.pk)
        # фильтрация комментарий под постом
        comments = Comment.objects.filter(user=self.name)

        self.rating = 0
        # цикл постов
        for post in posts:
            # лайки собранные поставми * 3
            self.rating += post.rating * 3
            # фильтрация комментарий для каждого поста
            post_comments = Comment.objects.filter(post=post)
            # цикл комментарий под каждым постом
            for post_comment in post_comments:
                # суммирование лайков комментарий
                self.rating += post_comment.rating
        # цикл комментарий оставленым автором
        for comment in comments:
            # суммирование комментарий
            self.rating += comment.rating
        # сохранение рейтинга в БД
        self.save()


class Category(models.Model):
    """Категории"""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    descriptions = models.TextField(default='Описание пока нету')
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="UR")
    subscribers = models.ManyToManyField(
        User, blank=True, related_name="categories")

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('CategoryDetail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)


class Subscription(models.Model):
    '''Подписки на посты категорий'''
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return f'{self.user}({self.category})'


class Comment(models.Model):
    """Комментарии"""

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text} => {self.post}'


class PostCategory(models.Model):
    """Модель связи между Постами и Категориями"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Пост/Категория'
        verbose_name_plural = 'Посты/Категории'

    def __str__(self):
        return f'{self.post}, {self.category.name}'
