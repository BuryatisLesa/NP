from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """Таблица для постов"""
    news = 'NS'
    art = 'AT'
    blank = [(news, 'новость'),
             (art, 'статья')]
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=blank, default='NS')
    title = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1000)
    category = models.ManyToManyField('Category', through='PostCategory', blank = True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += 1
        self.save()

    def preview(self):
        return f'{self.content[:124]}...'


class Author(models.Model):
    """Таблица для авторов"""
    name = models.OneToOneField('User', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{User.objects.get(pk=self.name.pk)}'

    def update_rating(self):
        posts = Post.objects.filter(author_id=self.pk)
        comments = Comment.objects.filter(user=self.name)

        self.rating = 0
        for post in posts:
            self.rating += post.rating * 3
            post_coments = Comment.objects.filter(post=post)
            for post_comment in post_coments:
                self.rating += post_comment.rating

        for comment in comments:
            self.rating += comment.rating

        self.save()


class User(User):
    """Таблица пользователей"""
    pass


class Category:
    """Таблица категорий"""
    name = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)


class Comment:
    """Таблица комментарий"""
    post_id = models.ForeignKey(Post, on_delete=None)
    user_id = models.ForeignKey(User, on_delete=None)
    text = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)


class PostCategory(models.Model):
    """Many to Many"""
    post_id = models.ForeignKey(Post, on_delete=None)
    category_id = models.ForeignKey(Category, on_delete=None)

