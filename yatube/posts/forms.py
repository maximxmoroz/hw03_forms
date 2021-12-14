from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """
    Форма для добавления новой записи.
    """
    class Meta:
        model = Post
        fields = ('text', 'group')
