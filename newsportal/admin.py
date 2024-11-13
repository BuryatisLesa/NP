from django.contrib import admin
from .models import (Post, Category, Comment, PostCategory,
                     Author, Subscription)
from modeltranslation.admin import TranslationAdmin


class PostAdmin(TranslationAdmin, admin.ModelAdmin):
    model = Post
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('author', 'type', 'title', 'date', 'content')
    # list_filter = ('type', 'category')
    search_fields = ('title', 'category__name')
    # actions = []
class PostTranslation(TranslationAdmin):
    model = Post

class CategoryAdmin(TranslationAdmin, admin.ModelAdmin):
    model = Category
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(Author)
admin.site.register(Subscription)
