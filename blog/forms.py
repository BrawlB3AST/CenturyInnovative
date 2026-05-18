from django import forms
from django.forms.widgets import FileInput
from .models import Post, Comment


# ── Custom widget that allows multiple file selection ─────────────────────
class MultipleFileInput(FileInput):
    def __init__(self, attrs=None):
        # bypass Django 6's multiple-file block by NOT calling super().__init__
        # with multiple in attrs — we set it directly on the HTML element
        super(FileInput, self).__init__(attrs)   # skip FileInput.__init__ check

    def use_required_attribute(self, initial_value):
        return False

    def value_from_datadict(self, data, files, name):
        return files.getlist(name)   # return list, not single file

    def value_omitted_from_data(self, data, files, name):
        return False


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput(attrs={
            'accept': 'image/*,video/mp4',
        }))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # data is already a list from value_from_datadict
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


# ── Forms ─────────────────────────────────────────────────────────────────
class PostForm(forms.ModelForm):
    media_files = MultipleFileField(
        required=False,
        label='Images / Video',
        help_text='Select up to 10 images and/or one MP4.',
    )

    class Meta:
        model  = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows':        4,
                'placeholder': "What's on your mind?",
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows':        2,
                'placeholder': 'Write a comment…',
            })
        }