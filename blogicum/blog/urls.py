from django.urls import include, path

from . import views

app_name = "blog"

post_urls = [
    path("<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("create/", views.PostCreateView.as_view(), name="create_post"),
    path(
        "<int:pk>/edit/",
        views.PostUpdateView.as_view(),
        name="edit_post",
    ),
    path(
        "<int:pk>/delete/",
        views.PostDeleteView.as_view(),
        name="delete_post",
    ),
]

comments_urls = [
    path(
        "<int:pk>/comment/",
        views.CommentCreateView.as_view(),
        name="add_comment",
    ),
    path(
        "<int:pk>/edit_comment/<int:comment_id>",
        views.CommentUpdateView.as_view(),
        name="edit_comment",
    ),
    path(
        "<int:pk>/delete_comment/<int:comment_id>",
        views.CommentDeleteView.as_view(),
        name="delete_comment",
    ),
]

urlpatterns = [
    path(
        "posts/",
        include(
            post_urls,
        ),
    ),
    path(
        "posts/",
        include(
            comments_urls,
        ),
    ),
    path(
        "category/<slug:category_slug>/",
        views.CategoryListView.as_view(),
        name="category_posts",
    ),
    path("profile/edit_profile/",
         views.EditProfileView.as_view(),
         name="edit_profile"
         ),
    path("profile/<str:username>/",
         views.PostListView.as_view(),
         name="profile"
         ),
    path("", views.IndexListView.as_view(), name="index"),
]
