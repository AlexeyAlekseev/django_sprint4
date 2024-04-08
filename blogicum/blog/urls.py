from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/',
         views.CategoryDetailView.as_view(), name='category_posts'),
    path('posts/create', views.create_post, name='create_post'),
    path('profile/<slug:username>', views.profile, name='profile'),
]
