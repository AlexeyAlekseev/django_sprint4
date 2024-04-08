from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import QuerySet, Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView
from django.views.generic.list import MultipleObjectMixin

from blog.forms import PostForm, CommentsForm
from blog.models import Category, Post, User, Comment

MAX_POSTS_LIMIT = 5


def get_post_list(category: Optional[Category] = None) -> 'QuerySet[Post]':
    """
    Return a queryset of published posts with specific category (if provided).

    :param category: Optional parameter, filtering posts by category.
    :return: Queryset of published posts.
    """
    query = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).only(
        'title',
        'text',
        'pub_date',
        'author__username',
        'location__name',
        'category__title',
        'category__slug',
        'location__is_published'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True
    )
    query = query.filter(
        category=category
    ) if category is not None else query.filter(
        category__is_published=True
    )
    return query


def get_unfiltred_post(
        category: Optional[Category] = None) -> 'QuerySet[Post]':
    """
    Return a queryset of published posts with specific category (if provided).

    :param category: Optional parameter, filtering posts by category.
    :return: Queryset of published posts.
    """
    query = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).only(
        'title',
        'text',
        'pub_date',
        'author__username',
        'location__name',
        'category__title',
        'category__slug',
        'location__is_published'
    )
    if category is not None:
        return query.filter(category=category)
    return query


class IsAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class PostListView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Post]:
        return get_post_list().annotate(
            comment_count=Count('comments')).order_by('-pub_date')


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    queryset = get_unfiltred_post()

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if (
                post.is_published and post.category.is_published and post.pub_date <= timezone.now()) or self.request.user == post.author:
            return post
        else:
            raise Http404("Post does not exist or is not published")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CategoryDetailView(DetailView, MultipleObjectMixin):
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    queryset = Category.objects.only('id', 'description', 'title',
                                     'slug').filter(is_published=True)
    paginate_by = 10

    def get_context_data(self, **kwargs):
        category = self.get_object()
        post_list = get_unfiltred_post(
            category=category).filter(pub_date__lte=timezone.now(),
                                      is_published=True).annotate(
            comment_count=Count('comments')).order_by('-pub_date')
        context = super(CategoryDetailView, self).get_context_data(
            object_list=post_list, **kwargs)
        return context


"""------------------USER PROFILE ---------------------------"""


class UserProfileDetailView(DetailView, MultipleObjectMixin):
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username'
    paginate_by = 10

    def get_object(self, **kwargs):
        return get_object_or_404(User,
                                 username=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        author = self.get_object()
        post_list = get_unfiltred_post().filter(author=author).annotate(
            comment_count=Count('comments')).order_by('-pub_date')
        context = super(UserProfileDetailView, self).get_context_data(
            object_list=post_list, **kwargs
        )
        context['profile'] = author
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'email']
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.object.username}
        )

    def test_func(self):
        return self.get_object().username == self.request.user


"""------------------POST CREATE/UPDATE/DELETE ---------------------------"""


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return redirect('blog:post_detail', id=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})


class PostUpdateView(LoginRequiredMixin, IsAuthorMixin, UpdateView):
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, **kwargs):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})


class PostDeleteView(LoginRequiredMixin, IsAuthorMixin, DeleteView):
    template_name = 'blog/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.get_object())
        return context

    def get_object(self, **kwargs):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})


"""----------------- COMMENTS CREATE/UPDATE/DELETE ------------------------"""


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentsForm
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.object.post.id})


class CommentUpdateView(LoginRequiredMixin, IsAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentsForm
    template_name = 'blog/comment.html'
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_id'
    comment = None
    comment_id = None
    post_id = None

    def dispatch(self, request, *args, **kwargs):
        self.post_id = self.kwargs['post_id']
        self.comment_id = self.kwargs['comment_id']
        self.comment = get_object_or_404(Comment, id=self.comment_id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'post_id': self.post_id,
            'comment_id': self.comment_id,
            'comment': self.comment,
        })
        return context

    def form_valid(self, form):
        form.save()
        send_mail(
            subject='New comment',
            message=f'опубликован новый коммент!',
            from_email='noreplay@acme.not',
            recipient_list=['root@acme.not'],
            fail_silently=True,
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.post_id})


class CommentDeleteView(LoginRequiredMixin, IsAuthorMixin, DeleteView):
    template_name = 'blog/comment.html'

    def get_object(self, **kwargs):
        return get_object_or_404(Comment, id=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})
