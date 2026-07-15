from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'content']
        labels = {
            'title': 'タイトル',
            'image': '画像',
            'content': '本文',
        }
        error_messages = {
            'title': {
                'required': 'タイトルを入力してください。',
            },
            'image': {
                'required': '画像をアップロードしてください。',
            },
            'content': {
                'required': '本文を入力してください。',
            },
        }
