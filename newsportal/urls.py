from django.urls import path
from . import views
from .views import (PostList,
                    NewsList,
                    PostCreate,
                    ArticleList,
                    PostUpdate,
                    PostDelete,
                    CategoryList,
                    ProfileList,
                    subscriptions,
                    post_detail)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', PostList.as_view(), name='HomePage'),
    path('<slug:slug>', views.post_detail, name='PostDetail'),
    path('news/', NewsList.as_view(), name='NewsList'),
    path('news/<slug:slug>', views.post_detail, name='NewsDetail'),
    path('articles/', ArticleList.as_view(), name='ArticlesList'),
    path('articles/<slug:slug>', views.post_detail, name='ArticlesDetail'),
    path('create/',PostCreate.as_view(), name='PostCreate'),
    path('<slug:slug>/update/',PostUpdate.as_view(), name='PostUpdate'),
    path('<slug:slug>/delete/',PostDelete.as_view(), name='PostDelete'),
    path('categories/', CategoryList.as_view(), name='CategoryList'),
    path('accounts/login/profile/', ProfileList.as_view(), name='profile'),
    path('subscriptions/', subscriptions, name='subscriptions'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)