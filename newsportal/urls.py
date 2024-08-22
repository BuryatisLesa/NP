from django.urls import path
from .views import *


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('news/', NewsList.as_view()),
    path('news/<int:pk>', PostDetail.as_view()),
    path('articles/', ArticleList.as_view()),
    path('articles/<int:pk>', PostDetail.as_view()),
]