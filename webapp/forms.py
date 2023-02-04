from django import forms
from django.forms import widgets
from webapp.models import Tag, Article, Comment


class ArticleForm(forms.ModelForm):
    title = forms.CharField()
    author = forms.CharField()
    text = forms.CharField(widget=widgets.Textarea)
    tags = forms.ModelMultipleChoiceField(required=False, label='Теги', queryset=Tag.objects.all())

    class Meta:
        model = Article
        fields = ['title', 'author', 'text']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
