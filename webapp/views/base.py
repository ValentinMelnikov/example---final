from urllib.parse import urlencode

from django.db.models import Q
from django.views.generic import RedirectView, ListView

from webapp.forms import SimpleSearchForm
from webapp.models import Article


class IndexRedirectView(RedirectView):
    pattern_name = 'index'


class IndexView(ListView):
    template_name = 'webapp/article/index.html'
    context_object_name = 'articles'
    paginate_by = 5
    paginate_orphans = 1
    model = Article
    ordering = ['-created_at']

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(title__icontains=self.search_value) | Q(author__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None
