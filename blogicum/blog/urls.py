from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('posts/<int:id>/', views.PostDetail.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/',
         views.CategoryPosts.as_view(),
         name='category_posts'),
    path(
        'profile/edit/',
        views.EditProfile.as_view(),
        name='edit_profile'),
    path(
        'profile/<slug:username>/',
        views.Profile.as_view(),
        name='profile'),
    path(
        'posts/create/',
        views.CreatePost.as_view(),
        name='create_post'),
    path(
        'posts/<int:id>/edit/',
        views.EditPost.as_view(),
        name='edit_post'),
    path(
        'posts/<id>/delete/',
        views.DeletePost.as_view(),
        name='delete_post'),
    path('posts/<int:id>/comment/',
         views.CreateComment.as_view(),
         name='add_comment'),
    path('posts/<int:id>/edit_comment/<int:comment_id>/',
         views.EditComment.as_view(),
         name='edit_comment'),
    path('posts/<int:id>/delete_comment/<int:comment_id>/',
         views.DeleteComment.as_view(),
         name='delete_comment'),
]
