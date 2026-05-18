from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class':       'input-field',
                'placeholder': field.label,
            })


class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ['title', 'content', 'image']


class ProfileForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ['bio', 'avatar_initial_color', 'website', 'twitter']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows':        3,
                'placeholder': 'Tell the community about yourself…',
            }),
            'avatar_initial_color': forms.TextInput(attrs={'type': 'color'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://yoursite.com'}),
            'twitter': forms.TextInput(attrs={'placeholder': '@handle'}),
        }
        labels = {
            'avatar_initial_color': 'Avatar colour',
        }
