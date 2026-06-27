from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        labels = {
            'title': 'タイトル',
            'content': '本文',
        }
        error_messages = {
            'title': {
                'required': 'タイトルを入力してください。',
            },
            'content': {
                'required': '本文を入力してください。',
            },
        }
