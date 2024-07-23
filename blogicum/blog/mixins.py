from django.db.models import Count
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from blog.constants import POST_LIST_LIMIT
from blog.form import CommentsForm, PostForm
from blog.models import Comments, Post


class PostListMixin:
    model = Post
    paginate_by = POST_LIST_LIMIT

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (
            queryset.select_related("category")
            .annotate(comment_count=Count("comments"))
            .filter(
                category__is_published=True,
                is_published=True,
                pub_date__lte=timezone.now(),
            )
            .order_by("-pub_date")
        )
        return queryset


class PostMixin:
    model = Post
    template_name = "blog/create.html"
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            return redirect("blog:post_detail", pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("blog:profile", kwargs={"username": self.request.user.username})


class CommentsMixin:
    model = Comments
    form_class = CommentsForm
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"

    def get_object(self):
        comment = super().get_object()
        if comment.author != self.request.user:
            raise Http404
        return comment

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.kwargs["pk"]})