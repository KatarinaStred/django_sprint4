from django.db.models import Count
from django.utils import timezone

from blog.models import Post


def get_post_list():
    """Получение списка всех постов."""
    return Post.objects.select_related(
        'author',
        'category',
        'location'
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')


def get_published_post_list():
    """Получение списка всех опубликованных постов."""
    return get_post_list().filter(
        category__is_published=True,
        is_published=True,
        pub_date__lt=timezone.now()
    )
