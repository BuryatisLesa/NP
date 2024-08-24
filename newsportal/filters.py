from django_filters import FilterSet, DateTimeFilter
from .models import *
from django.forms import DateTimeInput


class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='date',
        lookup_expr='lt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'}
        )
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'category': ['exact'],
        }

    label = {
        'title':'Заголовок'
    }
