from django import forms
from django.core.exceptions import ValidationError

from .models import Comment


class ShareForm(forms.Form):
    name = forms.CharField(
        max_length=64, widget=forms.TextInput(attrs={'placeholder': 'name'})
    )
    content = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'placeholder': 'content'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'your email'}),
        initial='a@a.com',
    )
    email_to = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'receiver email'}),
        initial='a@a.com',
    )

    def clean_name(self) -> str:
        name = self.cleaned_data['name']
        if len(name) >= 20:
            raise ValidationError('Name len must be less than 20')
        return name


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'placeholder': 'content',
                    'cols': 30,
                    'rows': 3,
                }
            )
        }
