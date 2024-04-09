"""Blog views."""
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet, Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.views.generic.list import MultipleObjectMixin

from blog.forms import PostForm, CommentsForm
from blog.models import Category, Post, User, Comment


def get_posts(published=None, category=None,
              author=None) -> 'QuerySet[Post]':
    """Get queryset with filtered posts."""
    queryset = Post.objects.prefetch_related(
        'category',
        'location',
        'author'
    ).select_related(
        'author',
        'category',
        'location'
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')
    if published is not None:
        return queryset.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
    elif category is not None:
        return queryset.filter(
            category=category,
            pub_date__lte=timezone.now(),
            is_published=True
        )
    elif author is not None:
        return queryset.filter(author=author)

    else:
        return queryset


class IsAuthorMixin(UserPassesTestMixin):
    """Mixin for checking if user is authenticated."""

    def test_func(self):
        """Check user is author."""
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        """Redirect to login page if user is not authenticated."""
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class PostListView(ListView):
    """View for listing posts."""

    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10
    queryset = get_posts(published=True)


class PostDetailView(DetailView):
    """View for showing post-details."""

    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    queryset = get_posts()

    def get_object(self, queryset=None):
        """Get post object."""
        post = super().get_object(queryset)
        if ((
                post.is_published
                and post.category.is_published
                and post.pub_date <= timezone.now())
                or self.request.user == post.author):
            return post
        else:
            raise Http404('Пост не найден')

    def get_context_data(self, **kwargs):
        """Get post context."""
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CategoryDetailView(DetailView, MultipleObjectMixin):
    """View for showing category details."""

    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    queryset = Category.objects.filter(is_published=True)
    paginate_by = 10
    print(queryset)

    def get_context_data(self, **kwargs):
        """Get category context."""
        category = self.get_object()
        post_list = get_posts(category=category)
        context = super(CategoryDetailView, self).get_context_data(
            object_list=post_list, **kwargs)
        return context


class UserProfileDetailView(DetailView, MultipleObjectMixin):
    """View for showing user profile details."""

    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username'
    paginate_by = 10

    def get_object(self, **kwargs):
        """Get user profile object."""
        return get_object_or_404(User,
                                 username=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        """Get user profile context."""
        author = self.get_object()
        post_list = get_posts(author=author)
        context = super(UserProfileDetailView, self).get_context_data(
            object_list=post_list, **kwargs
        )
        context['profile'] = author
        context['user'] = self.request.user
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating user profile."""

    model = User
    fields = ['first_name', 'last_name', 'username', 'email']
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        """Get user profile object."""
        return self.request.user

    def get_success_url(self):
        """Redirect to user pofile page."""
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.object.username}
        )

    def test_func(self):
        """Check user is author."""
        return self.get_object().username == self.request.user


class UserRegistrationView(CreateView):
    """View for creating new user."""

    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        """Validate form."""
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


class PostCreateView(LoginRequiredMixin, CreateView):
    """View for creating new post."""

    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        """Validate form."""
        if not self.request.user.is_authenticated:
            return redirect('blog:post_detail', id=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to user profile page."""
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})


class PostUpdateView(LoginRequiredMixin, IsAuthorMixin, UpdateView):
    """View for updating post."""

    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, **kwargs):
        """Get post object."""
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def form_valid(self, form):
        """Validate form."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to user profile page."""
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})


class PostDeleteView(LoginRequiredMixin, IsAuthorMixin, DeleteView):
    """View for deleting post."""

    template_name = 'blog/create.html'

    def get_context_data(self, **kwargs):
        """Get post context."""
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.get_object())
        return context

    def get_object(self, **kwargs):
        """Get post object."""
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_success_url(self):
        """Redirect to user profile page."""
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})


class CommentCreateView(LoginRequiredMixin, CreateView):
    """View for comments create."""

    form_class = CommentsForm
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        """Validate form."""
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to post page."""
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.object.post.id})


class CommentUpdateView(LoginRequiredMixin, IsAuthorMixin, UpdateView):
    """View for comment update."""

    model = Comment
    queryset = Comment.objects.select_related('author')
    form_class = CommentsForm
    template_name = 'blog/comment.html'
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_id'
    comment = None
    comment_id = None
    post_id = None

    def dispatch(self, request, *args, **kwargs):
        """Dispatch func."""
        self.post_id = self.kwargs['post_id']
        self.comment_id = self.kwargs['comment_id']
        self.comment = get_object_or_404(Comment, id=self.comment_id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Get post context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'post_id': self.post_id,
            'comment_id': self.comment_id,
            'comment': self.comment,
        })
        return context

    def form_valid(self, form):
        """Validate form."""
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to post page."""
        return reverse('blog:post_detail', kwargs={'post_id': self.post_id})


class CommentDeleteView(LoginRequiredMixin, IsAuthorMixin, DeleteView):
    """View for comment delete."""

    template_name = 'blog/comment.html'

    def get_object(self, **kwargs):
        """Get post object."""
        return get_object_or_404(Comment, id=self.kwargs['comment_id'])

    def get_success_url(self):
        """Redirect to post page."""
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})
