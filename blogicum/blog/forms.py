from django import forms
from django.utils import timezone

from .models import Comment, Post, User


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'created_at',)
        widgets = {
            'pub_date': forms.DateTimeInput(format='%Y-%m-%dT%H:%M',
                                            attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.localtime(
            timezone.now()
        ).strftime('%Y-%m-%dT%H:%M')


class CreateCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(CreateCommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['cols'] = 10
        self.fields['text'].widget.attrs['rows'] = 5


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
