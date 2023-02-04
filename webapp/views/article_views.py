from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from django.views.generic import TemplateView, FormView, DetailView

from webapp.forms import ArticleForm
from webapp.models import Article


# class ArticleView(TemplateView):
#     template_name = 'webapp/article/detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['article'] = get_object_or_404(Article, pk=kwargs['pk'])
#         return context

class ArticleView(DetailView):
    template_name = 'webapp/article/detail.html'
    model = Article


class AddArticleView(TemplateView):
    template_name = 'webapp/article/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ArticleForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data.pop('tags')
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text']
            )
            article.tags.set(tags)
            return redirect('article_view', pk=article.pk)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


# class UpdateArticleView(TemplateView):
#     template_name = 'webapp/article/update.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         article = get_object_or_404(Article, pk=kwargs['pk'])
#         form = ArticleForm(instance=article)
#         context['form'] = form
#         context['article'] = article
#         return context
#
#     def post(self, request, *args, **kwargs):
#         article = get_object_or_404(Article, pk=kwargs['pk'])
#         form = ArticleForm(request.POST)
#         if form.is_valid():
#             tags = form.cleaned_data.pop('tags')
#             article.title = form.cleaned_data['title']
#             article.author = form.cleaned_data['author']
#             article.text = form.cleaned_data['text']
#             article.save()
#             article.tags.set(tags)
#             return redirect('article_view', pk=article.pk)
#         else:
#             context = self.get_context_data(**kwargs)
#             context['form'] = form
#             return self.render_to_response(context)


class DeleteArticle(TemplateView):
    template_name = 'webapp/article/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, pk=kwargs['pk'])
        context['article'] = article
        return context

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        article.delete()
        return redirect('index')


class ArticleUpdateView(FormView):
    template_name = 'webapp/article/update.html'
    form_class = ArticleForm

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.article
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.article
        return kwargs

    def form_valid(self, form):
        tags = form.cleaned_data.pop('tags')
        for key, value in form.cleaned_data.items():
            if value is not None:
                setattr(self.article, key, value)
        self.article.save()
        self.article.tags.set(tags)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.article.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)




