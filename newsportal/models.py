from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify
from time import time


def gen_slug(string):
    '''метод для создание слага для постов и категорий, и т.д.'''
    finally_slug = slugify(string, allow_unicode=False,) # функция по генерации слага
    return finally_slug + '-' + str(int(time())) # финальный слага + время создания


class Post(models.Model):
    """Посты"""

    class Meta:
        verbose_name = 'Пост' # мета данные ед.ч.
        verbose_name_plural = 'Посты' # мета данные мн.ч

    NEWS = 'NS' # переменная типа новостей
    ARTICLE = 'AT' # переменная типа статей
    POST_TYPE_CHOICES = [(NEWS, 'Новость'),
                         (ARTICLE, 'Статья')]
    author = models.ForeignKey('Author', on_delete=models.CASCADE) # столбец авторов
    type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES, default='NS') # столбец типа поста
    title = models.CharField(max_length=150) # столбец заголовка поста
    date = models.DateTimeField(auto_now_add=True) # столбец для даты создания поста
    content = models.TextField() # столбец содержащий контент для поста
    category = models.ManyToManyField('Category', through='PostCategory', blank=False) # категории поста
    rating = models.IntegerField(default=0) # рейтинг поста
    image = models.ImageField(upload_to='images/', null=True, blank=True) # картинка поста
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL") # созданный слаг для поста на основе заголовка

    def save(self, *args, **kwargs):
        '''сохранение слага в БД'''
        self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        '''абсолютная ссылка на пост при использование в проекте'''
        return reverse('PostDetail', kwargs={'slug': self.slug})

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:124]}...'

    def __str__(self):
        return f'{self.title}, {self.category}, {self.type}'


class Author(models.Model):
    """Авторы"""

    class Meta:
        verbose_name = 'Автор' # мета данные ед.ч
        verbose_name_plural = 'Авторы' # мета данные мн.ч

    name = models.OneToOneField(User, on_delete=models.CASCADE) # столбец с никнеймом автора
    rating = models.IntegerField(default=0) # столбец для подсчёта рейтинга автора на основе его постов и комментарий


    def __str__(self):
        return f'{User.objects.get(pk=self.name.pk)}'

    def update_rating(self):
        '''обновление и суммирование рейтинга'''
        posts = Post.objects.filter(author_id=self.pk) # фильтрация постов созданным автором
        comments = Comment.objects.filter(user=self.name) # фильтрация комментарий под постом

        self.rating = 0
        for post in posts: # цикл постов
            self.rating += post.rating * 3 # лайки собранные поставми * 3
            post_comments = Comment.objects.filter(post=post) # фильтрация комментарий для каждого поста
            for post_comment in post_comments: # цикл комментарий под каждым постом
                self.rating += post_comment.rating # суммирование лайков комментарий

        for comment in comments: # цикл комментарий оставленым автором
            self.rating += comment.rating # суммирование комментарий 

        self.save() # сохранение рейтинга в БД


class Category(models.Model):
    """Категории"""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    descriptions = models.TextField(default='Описание пока нету')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

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

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='subscriptions')

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
        return f'{self.post}'
