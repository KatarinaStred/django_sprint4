from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView
)

from blog.forms import CreateCommentForm, CreatePostForm, ProfileForm
from blog.mixins import (
    ListPostsMixin, WorkCommentsMixin, WorkPostsMixin
)
from blog.models import Category, Comment, Post
from core.service import get_post_list, get_published_post_list

User = get_user_model()


class Index(ListPostsMixin):
    """Отображение постов на главной странице."""


class CreatePost(LoginRequiredMixin, CreateView):
    """Создание поста."""

    model = Post
    form_class = CreatePostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def form_valid(self, form):
        """Запись автора."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class EditPost(WorkPostsMixin, UpdateView):
    """Редактирование поста автором."""

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.pk})


class DeletePost(WorkPostsMixin, DeleteView):
    """Удаление поста автором."""

    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreatePostForm(instance=self.object)
        return context


class PostDetail(DetailView):
    """Отображение одного из существующих постов."""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self):
        post = super().get_object()
        if self.request.user == post.author:
            return post
        return get_object_or_404(
            get_published_post_list(),
            id=post.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateCommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CategoryPosts(ListPostsMixin):
    """Определение категории публикации."""

    template_name = 'blog/category.html'
    category = None

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs.get('category_slug'))
        return get_published_post_list().filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs.get('category_slug')
        )
        return context


class Profile(ListPostsMixin):
    """Отображение списка постов в профиле."""

    template_name = 'blog/profile.html'
    form_class = ProfileForm

    def get_queryset(self):
        author = get_object_or_404(
            User,
            username=self.kwargs['username'])
        if self.request.user != author:
            return get_published_post_list().filter(author=author)
        return get_post_list().filter(author=author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(User, username=self.kwargs.get(
            'username'
        ))
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditProfile(LoginRequiredMixin, UpdateView):
    """Редактирование профиля."""

    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CreateComment(LoginRequiredMixin, CreateView):
    """Добавление комментария."""

    model = Comment
    form_class = CreateCommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditComment(WorkCommentsMixin,
                  UpdateView):
    """Редактирование комментария."""

    form_class = CreateCommentForm


class DeleteComment(WorkCommentsMixin,
                    DeleteView):
    """Удаление комментария."""

    pass
