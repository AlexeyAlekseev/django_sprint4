"""
The `blog/apps.py` module defines the `BlogConfig`
class which is used by Django
to configure the 'blog' application.
"""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Django App Configuration for the 'blog' application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Блог'
