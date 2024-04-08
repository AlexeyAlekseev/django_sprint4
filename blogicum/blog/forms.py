from django import forms

from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'location', 'pub_date', 'image')

        widgets = {
            'pub_date': forms.DateInput(format='%Y-%m-%d %H:%M:%S',
                                        attrs={'type': 'datetime-local',
                                               'class': 'form-control'}, )
        }


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
