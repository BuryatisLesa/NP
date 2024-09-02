from django import forms
from .models import *
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-create', 'placeholder':'Заголовок'}))
    type = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-create'}), choices=Post.POST_TYPE_CHOICES)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-create', 'placeholder': 'Текст'}))
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-create'}))
    image = forms.ImageField()

    class Meta:
        model = Post
        fields = [
            'title',
            'type',
            'content',
            'category',
            'image',
            'author'
        ]
        # widgets = {'author': forms.HiddenInput()}

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        if content is not None and len(content) < 20:
            raise ValidationError({
                "content": "Описание не может быть менее 20 символов."
            })

        return cleaned_data

    def clean_title(self):
        name = self.cleaned_data["title"]
        if name[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return name

