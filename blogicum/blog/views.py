from django.shortcuts import get_object_or_404, redirect
from blog.models import Post, Category, Comment
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.urls import reverse, reverse_lazy
from .forms import ProfileForm, CreatePostForm, CreateCommentForm
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


PAGINATOR_COUNT = 10

User = get_user_model()


def get_post_list():
    """Получение списка всех постов"""
    return Post.objects.select_related(
        'author',
        'category',
        'location'
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')


def get_published_post_list():
    """Получение списка всех опубликованных постов"""
    return get_post_list().filter(
        category__is_published=True,
        is_published=True,
        pub_date__lt=timezone.now()
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')


class ListPostsMixin(ListView):
    """Формирование списка постов"""

    model = Post
    template_name = 'blog/index.html'
    paginate_by = PAGINATOR_COUNT

    def get_queryset(self):
        return get_published_post_list(
        )


class OnlyAuthorMixin(UserPassesTestMixin):
    """Определение является ли пользователь автором публикации."""

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return reverse('blog:post_detail', args=[self.kwargs['id']])


class WorkPostsMixin(OnlyAuthorMixin):
    """Работа с публикациями"""

    model = Post
    form_class = CreatePostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', id=self.kwargs['id'])
        return super().dispatch(request, *args, **kwargs)


class WorkCommentsMixin(OnlyAuthorMixin):
    """Работа с комментариями"""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['id']])

    def dispatch(self, request, **kwargs):
        instance = get_object_or_404(Comment, id=self.kwargs['comment_id'])
        if instance.author != self.request.user:
            return redirect('blog:post_detail', id=self.kwargs['id'])
        return super().dispatch(request, **kwargs)


class Index(ListPostsMixin):
    """Отображение постов на главной странице."""

    pass


class CreatePost(LoginRequiredMixin, CreateView):
    """Создание поста."""

    model = Post
    form_class = CreatePostForm
    pk_url_kwarg = 'id'
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
        return reverse('blog:post_detail', kwargs={'id': self.object.id})


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
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['id'])
        if self.request.user == post.author:
            return post
        return get_object_or_404(
            get_published_post_list(),
            id=self.kwargs['id'])

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
        context['category'] = get_object_or_404(Category.objects.filter(
            is_published=True),
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
        return reverse_lazy(
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
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        return dict(**super().get_context_data(**kwargs),
                    form=CreateCommentForm())

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['id']])

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['id'])
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['id']
        return super().form_valid(form)


class EditComment(WorkCommentsMixin, UpdateView):
    """Редактирование комментария."""

    form_class = CreateCommentForm


class DeleteComment(WorkCommentsMixin, DeleteView):
    """Удаление комментария."""

    pass
