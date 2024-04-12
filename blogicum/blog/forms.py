"""Form classes."""
from django import forms

from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    """The Form for creating a Post instance."""

    class Meta:
        """A meta class that configures additional parameters of the model."""

        model = Post
        fields = (
            'title', 'text', 'category', 'location', 'pub_date', 'image',
        )

        widgets = {
            'pub_date': forms.DateInput(format='%Y-%m-%d %H:%M:%S',
                                        attrs={'type': 'datetime-local',
                                               'class': 'form-control'}, )
        }


class CommentsForm(forms.ModelForm):
    """The Form for creating a Comment instance."""

    class Meta:
        """A meta class that configures additional parameters of the model."""

        model = Comment
        fields = ('text',)
