from django.urls import path
from . import views
from .views import (PostList,
                    news_list,
                    PostCreate,
                    article_list,
                    PostUpdate,
                    PostDelete,
                    CategoryList,
                    ProfileList,
                    subscriptions,
                    post_detail,
                    category_detail)
from django.conf import settings
from django.conf.urls.static import static
# from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', PostList.as_view(), name='HomePage'),
    path('<int:pk>/<slug:slug>', views.post_detail, name='PostDetail'),
    path('news/', views.news_list, name='NewsList'),
    path('news/<int:pk>/<slug:slug>', views.post_detail, name='NewsDetail'),
    path('articles/', views.article_list, name='ArticlesList'),
    path('articles/<int:pk>/<slug:slug>', views.post_detail, name='ArticlesDetail'),
    path('create/', PostCreate.as_view(), name='PostCreate'),
    path('<int:pk>/<slug:slug>/update', PostUpdate.as_view(),
         name='PostUpdate'),
    path('<int:pk>/<slug:slug>/delete', PostDelete.as_view(), name='PostDelete'),
    path('categories/', CategoryList.as_view(), name='CategoryList'),
    path('accounts/login/profile', ProfileList.as_view(), name='profile'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('categories/<slug:slug>', views.category_detail,
         name='CategoryDetail')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
