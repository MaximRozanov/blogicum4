from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Prefetch, Count
from django.http import Http404
from django.urls import reverse_lazy, reverse

from blog.models import Category, Post, User, Comments
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from . import form
from .constants import POST_LIST_LIMIT

from django.contrib.auth.mixins import LoginRequiredMixin

from .form import PostForm, UserProfileForm, CommentsForm


class IndexListView(ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = POST_LIST_LIMIT

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(comment_count=Count('comments')).filter(
            category__is_published=True,
            is_published=True,
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    # exclude = ('author',)
    template_name = "blog/create.html"

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        context['form'] = CommentsForm()
        context['comments'] = self.object.comments.select_related('author')

        return context


class PostMixin:
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if post.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUpdateView(PostMixin, UpdateView):
    pass


class PostDeleteView(PostMixin, DeleteView):
    pass


class CategoryListView(ListView):
    model = Post
    template_name = "blog/category.html"
    paginate_by = POST_LIST_LIMIT
    allow_empty = False

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug, is_published=True, )
        return Post.objects.annotate(comment_count=Count('comments')).filter(
            category=self.category,
            is_published=True,
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return context


class ProfileDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        post_list = Post.objects.annotate(comment_count=Count('comments')).filter(author=user).order_by(
            '-pub_date')
        paginator = Paginator(post_list, POST_LIST_LIMIT)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email',)
    # form_class = UserProfileForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self):
        return self.request.user


class CommentsMixin:
    model = Comments
    form_class = CommentsForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comments, pk=kwargs['comment_id'])
        if comment.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comments
    form_class = CommentsForm


    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(CommentsMixin, UpdateView):
    pass


class CommentDeleteView(CommentsMixin, DeleteView):
    pass
