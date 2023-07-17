from django_filters import FilterSet, DateFilter, CharFilter
from django.forms import DateInput

from .models import Post


class PostFilter(FilterSet):
    date = DateFilter(
        field_name='dateCreation',
        label='Date (later)',
        lookup_expr='gt',
        widget=DateInput(
            attrs={
                'type': 'date',
            }
        ),
    )
    title = CharFilter(
        field_name='title',
        label='Title',
        lookup_expr='icontains',
    )
    author = CharFilter(
        field_name='author__authorUser__username',
        label='Author',
        lookup_expr='icontains',
    )

    class Meta:
        model = Post
        fields = []