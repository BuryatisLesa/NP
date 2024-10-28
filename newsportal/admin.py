from django.contrib import admin
from .models import Post, Category, Comment, PostCategory, Author, Subscription

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Post, PostAdmin)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(Author)
admin.site.register(Subscription)




