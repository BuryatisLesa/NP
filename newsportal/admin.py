from django.contrib import admin
from .models import (Post, Category, Comment, PostCategory,
                     Author, Subscription)


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('author', 'type', 'title', 'date', 'content')
    # list_filter = ('type', 'category')
    search_fields = ('title', 'category__name')
    # actions = []


admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(Author)
admin.site.register(Subscription)
