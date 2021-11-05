from django import forms
from .models import Post,Like

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption','image']
