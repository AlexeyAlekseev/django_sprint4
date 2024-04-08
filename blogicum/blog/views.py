from typing import Optional

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Category, Post
from django.views.generic import ListView, DetailView
from django.views.generic.list import MultipleObjectMixin

MAX_POSTS_LIMIT = 5


def get_post_list(category: Optional[Category] = None) -> 'QuerySet[Post]':
    """
    Return a queryset of published posts with specific category (if provided).

    :param category: Optional parameter, filtering posts by category.
    :return: Queryset of published posts.
    """
    query = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).only(
        'title',
        'text',
        'pub_date',
        'author__username',
        'location__name',
        'category__title',
        'category__slug',
        'location__is_published'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True
    )
    query = query.filter(
        category=category
    ) if category is not None else query.filter(
        category__is_published=True
    )
    return query


class PostListView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Post]:
        return get_post_list()


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    queryset = get_post_list()


class CategoryDetailView(DetailView, MultipleObjectMixin):
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    queryset = Category.objects.only('id', 'description', 'title', 'slug')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        category = self.get_object()
        post_list = get_post_list(category=category)
        context = super(CategoryDetailView, self).get_context_data(object_list=post_list, **kwargs)
        return context


def create_post(request):
    return None


def profile(request, username):
    return None
