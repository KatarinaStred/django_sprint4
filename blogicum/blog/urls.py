from django.urls import include, path

from . import views

app_name = 'blog'

posts_urls = [
    path(
        '<int:post_id>/',
        views.PostDetail.as_view(),
        name='post_detail'),
    path(
        'create/',
        views.CreatePost.as_view(),
        name='create_post'),
]

profile_urls = [
    path(
        'edit/',
        views.EditProfile.as_view(),
        name='edit_profile'),
    path(
        '<str:username>/',
        views.Profile.as_view(),
        name='profile'),
]

post_id_urls = [
    path(
        'edit/',
        views.EditPost.as_view(),
        name='edit_post'),
    path(
        'delete/',
        views.DeletePost.as_view(),
        name='delete_post'),
    path(
        'comment/',
        views.CreateComment.as_view(),
        name='add_comment'),
    path(
        'edit_comment/<int:comment_id>/',
        views.EditComment.as_view(),
        name='edit_comment'),
    path(
        'delete_comment/<int:comment_id>/',
        views.DeleteComment.as_view(),
        name='delete_comment'),
]


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('posts/', include(posts_urls)),
    path('posts/<int:post_id>/', include(post_id_urls)),
    path('profile/', include(profile_urls)),
    path('category/<slug:category_slug>/',
         views.CategoryPosts.as_view(),
         name='category_posts'),
]
