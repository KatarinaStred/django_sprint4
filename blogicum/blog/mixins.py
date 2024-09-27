from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView

from blog.constants import PAGINATOR_COUNT
from blog.forms import CreatePostForm
from blog.models import Comment, Post
from core.service import get_published_post_list


class ListPostsMixin(ListView):
    """Формирование списка постов."""

    model = Post
    template_name = 'blog/index.html'
    paginate_by = PAGINATOR_COUNT

    def get_queryset(self):
        return get_published_post_list()


class OnlyAuthorMixin(UserPassesTestMixin):
    """Определение является ли пользователь автором публикации."""

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class WorkPostsMixin(LoginRequiredMixin, OnlyAuthorMixin):
    """Работа с публикациями."""

    model = Post
    form_class = CreatePostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class WorkCommentsMixin(LoginRequiredMixin, OnlyAuthorMixin):
    """Работа с комментариями."""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])
