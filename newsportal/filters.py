from django_filters import FilterSet, DateTimeFilter, CharFilter
from .models import Post
from django.forms import DateTimeInput, TextInput


class PostFilter(FilterSet):
    # added_after = DateTimeFilter(
    #     field_name='date',
    #     lookup_expr='lt',
    #     widget=DateTimeInput(
    #         format='%Y-%m-%dT%H:%M',
    #         attrs={'type': 'datetime-local'}
    #     )
    # )

    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label=None,
        widget=TextInput(attrs={'placeholder': 'Введите заголовок', 'class': 'filter-input'})  # Убираем метку и добавляем placeholder
    )
    
    class Meta:
        model = Post
        fields = ['title']

    
