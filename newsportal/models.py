from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify
from time import time


def gen_slug(string):
    finally_slug = slugify(string, allow_unicode=False,)
    return finally_slug + '-' + str(int(time()))


class Post(models.Model):
    """Посты"""

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    NEWS = 'NS'
    ARTICLE = 'AT'
    POST_TYPE_CHOICES = [(NEWS, 'Новость'),
                         (ARTICLE, 'Статья')]
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES, default='NS')
    title = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    category = models.ManyToManyField('Category', through='PostCategory', blank=False)
    rating = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
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
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    name = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)


    def __str__(self):
        return f'{User.objects.get(pk=self.name.pk)}'

    def update_rating(self):
        posts = Post.objects.filter(author_id=self.pk)
        comments = Comment.objects.filter(user=self.name)

        self.rating = 0
        for post in posts:
            self.rating += post.rating * 3
            post_comments = Comment.objects.filter(post=post)
            for post_comment in post_comments:
                self.rating += post_comment.rating

        for comment in comments:
            self.rating += comment.rating

        self.save()


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
