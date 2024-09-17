from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from blog.models import Post, Category
from django.utils import timezone

MAX_POST_COUNT = 5


def get_post_list():
    """Получение списка постов с определенными фильтрами"""
    return Post.objects.select_related(
        'author',
        'category',
        'location'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=timezone.now()
    )


def index(request: HttpRequest) -> HttpResponse:
    """Отображение постов на главной странице."""
    return render(request,
                  'blog/index.html',
                  {'post_list': get_post_list()[:MAX_POST_COUNT]}
                  )


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Отображение одного из существующих постов."""
    post = get_object_or_404(
        get_post_list(),
        pk=id)
    return render(request,
                  'blog/detail.html',
                  {'post': post}
                  )


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Определение категории публикации."""
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug)
    post_list = get_post_list().filter(category=category)
    return render(request,
                  'blog/category.html',
                  {'category': category,
                   'post_list': post_list}
                  )
