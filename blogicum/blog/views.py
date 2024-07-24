from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q,
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.models import Category, Comment, Post, User
from blog.form import CommentForm, PostForm
from blog.mixins import CommentMixin, PostListMixin, PostMixin


class IndexListView(PostListMixin, ListView):
    template_name = "blog/index.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:profile",
                       kwargs={"username": self.request.user.username})


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"

    def get_object(self, queryset=None):
        obj = Post.objects.filter(
            Q(
                is_published=True,
                category__is_published=True,
                pub_date__lt=timezone.now(),
            )
            | Q(author=self.request.user)
        )
        return get_object_or_404(obj, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.select_related("author")
        return context


class PostUpdateView(LoginRequiredMixin, PostMixin, UpdateView):
    pass


class PostDeleteView(LoginRequiredMixin, PostMixin, DeleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(instance=self.object)
        return context


class CategoryListView(PostListMixin, ListView):
    template_name = "blog/category.html"

    def get_queryset(self):
        category_slug = self.kwargs["category_slug"]
        self.category = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True,
        )
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class PostListView(PostListMixin, ListView):
    template_name = "blog/profile.html"

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def get_queryset(self):
        user = self.get_object()
        if self.request.user == user:
            return PostListMixin.posts_queryset(self) \
                .filter(author__id=user.id)
        else:
            return super().get_queryset().filter(author=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["profile"] = profile
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )
    template_name = "blog/user.html"

    def get_success_url(self):
        return reverse("blog:profile", args=[self.request.user.username])

    def get_object(self):
        return self.request.user


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.kwargs["pk"]})


class CommentUpdateView(LoginRequiredMixin, CommentMixin, UpdateView):
    pass


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    pass
