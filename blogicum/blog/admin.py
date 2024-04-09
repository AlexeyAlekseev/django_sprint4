"""
`Blog/admin.py` module.
This module configures the administrative interface of the 'blog' app.
"""

from django.contrib import admin

from .models import Category, Location, Post, Comment

admin.site.empty_value_display = 'Не задано'


class CategoryAdmin(admin.ModelAdmin):
    """This class customizes the admin interface for the `Category` model."""

    list_display = (
        'title',
        'description',
        'slug',
        'is_published'
    )
    list_editable = (
        'is_published',
        'slug'
    )


class PostAdmin(admin.ModelAdmin):
    """This class customizes the admin interface for the `Post` model."""

    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published'
    )
    list_editable = (
        'is_published',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('category', 'location')
    list_display_links = ('title',)


class LocationAdmin(admin.ModelAdmin):
    """This class customizes the admin interface for the `Location` model."""

    list_display = (
        'name',
        'is_published'
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('name',)
    list_display_links = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
