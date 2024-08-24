from django.urls import path
from .views import PostList, NewsList, PostCreate, PostDetail, ArticleList, PostUpdate, PostDelete
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', PostList.as_view(), name='HomePage'),
    path('<int:pk>', PostDetail.as_view(), name='PostDetail'),
    path('news/', NewsList.as_view(), name='NewsList'),
    path('news/<int:pk>', PostDetail.as_view(), name='NewsDetail'),
    path('articles/', ArticleList.as_view(), name='ArticlesList'),
    path('articles/<int:pk>', PostDetail.as_view(), name='ArticlesDetail'),
    path('create/',PostCreate.as_view(), name='PostCreate'),
    path('<int:pk>/update/',PostUpdate.as_view(), name='PostUpdate'),
    path('<int:pk>/delete/',PostDelete.as_view(), name='PostDelete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)