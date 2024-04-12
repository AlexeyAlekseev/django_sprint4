"""Business logic utilities."""
import typing

from django.db.models import Count
from django.utils import timezone

from blog.constants import Config
from blog.models import Post

if typing.TYPE_CHECKING:
    from django.db.models import QuerySet  # noqa TC002


def get_posts(published=None, category=None,
              author=None) -> 'QuerySet[Post]':
    """Get queryset with filtered posts."""
    queryset = Post.objects.prefetch_related(
        'category',
        'location',
        'author'
    ).select_related(
        'author',
        'category',
        'location'
    ).annotate(
        comment_count=Count('comments')
    ).order_by(Config.ORDER_BY_DATE_DESC)
    if published is not None:
        return queryset.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
    elif category is not None:
        return queryset.filter(
            category=category,
            pub_date__lte=timezone.now(),
            is_published=True
        )
    elif author is not None:
        return queryset.filter(author=author)
    return queryset
