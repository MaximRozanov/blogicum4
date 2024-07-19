from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("category/<slug:category_slug>/",
         views.CategoryListView.as_view(),
         name="category_posts"),
    path(
        'posts/<int:pk>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post',
    ),
    path(
        'posts/<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post',
    ),
    path(
        'posts/<int:pk>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment',
    ),
    path(
        'posts/<int:pk>/edit_comment/<int:comment_id>',
        views.CommentUpdateView.as_view(),
        name='edit_comment',
    ),
    path(
        'posts/<int:pk>/delete_comment/<int:comment_id>',
        views.CommentDeleteView.as_view(),
        name='delete_comment',
    ),
    path('profile/edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', views.ProfileDetailView.as_view(), name='profile'),

    path("posts/create/", views.PostCreateView.as_view(), name="create_post")
]