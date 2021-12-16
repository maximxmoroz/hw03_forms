from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """
    Форма для добавления новой записи.
    """
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'group': 'Группа',
            'text': 'Текст поста',
        }
        help_texts = {
            'group': 'Выберите группу для публикации',
            'text': 'Поделитесь чем-нибудь увлекательным',
        }
