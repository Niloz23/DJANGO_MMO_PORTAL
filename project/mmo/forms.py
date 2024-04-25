from django import forms
from mmo.models import OneTimeCode, Post, Comment
from django.core.exceptions import ValidationError


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class MyActivationCodeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MyActivationCodeForm, self).__init__(*args, **kwargs)

    code = forms.CharField(required=True, max_length=50, label='Код подтверждения',
                           error_messages={'required': 'Введите код', 'max_lenght': 'Максимальное кол-во символов 50'})

    def save(self, commit=True):
        profile = super(MyActivationCodeForm, self).save(commit=False)
        profile.code = self.cleaned_data['code']
        profile.save()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'category',
            'head',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        head = cleaned_data.get("head")
        if head is not None and len(head) < 5:
            raise ValidationError({
                "head": "Заголовок не может быть менее 5 символов."
            })

        text = cleaned_data.get("text")
        if head == text:
            raise ValidationError(
                {
                    "text": "текст объявления не должен совпадать с заголовком"
                }
            )

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'post',
            'comment_text',
            'user',
        ]

class AcceptCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'is_acept',
        ]
        labels = {
            'is_acept': 'принять',
        }