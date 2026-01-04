from django import forms

from .models import Article, Comment, Category, Tag, Announcement

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content', 'category', 'tags', 'status')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment...'
            })
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'slug']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'is_active']