from django import forms
from .models import Category, Author, Post, User
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-create', 'placeholder':'Заголовок'}))
    type = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-create'}), choices=Post.POST_TYPE_CHOICES)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-create', 'placeholder': 'Текст'}))
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-create'}))
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = [
            'title',
            'type',
            'content',
            'category',
            'image',
        ]

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

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            author, created = Author.objects.get_or_create(name=user) # получаем или создает автора
            post.author = author
        if commit:
            post.save() # сохраняем пост
            self.save_m2m()  # Для сохранения категорий и других ManyToMany полей
        return post
