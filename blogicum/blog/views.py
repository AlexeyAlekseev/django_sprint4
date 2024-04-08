from typing import Optional

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Category, Post

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


def index(request: HttpRequest) -> HttpResponse:
    """Handles requests for the home page."""
    template: str = 'blog/index.html'
    post_list = get_post_list()[:MAX_POSTS_LIMIT]
    context: dict = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """Handles requests for displaying a specific post detail."""
    post = get_object_or_404(get_post_list(), id=post_id)
    context: dict = {'post': post}
    template: str = 'blog/detail.html'
    return render(request, template, context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """
    Handles requests for displaying posts
    belonging to a specific category.
    """
    category = get_object_or_404(
        Category.objects.only('id', 'description', 'title', 'slug'),
        slug=category_slug,
        is_published=True
    )

    post_list = get_post_list(category)

    context: dict = {'category': category, 'post_list': post_list}
    template: str = 'blog/category.html'
    return render(request, template, context)
