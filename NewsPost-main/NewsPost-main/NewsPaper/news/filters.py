from django_filters import FilterSet, ModelChoiceFilter
from .models import Post, Author


class PostFilter(FilterSet):
    author = ModelChoiceFilter(field_name='author', queryset=Author.objects.all(), label='Автор', empty_label='Любой')

    class Meta:
        model = Post
        fields = {
           'header': ['iexact'],
           'author': ['exact'],
           'date_in': ['iexact'],
            }
