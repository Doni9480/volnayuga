from django.shortcuts import render
from django.views.generic import DetailView
from page.models import Page
from seo.models import SeoPage


class PageDetail(DetailView):
    model = Page
    template_name = 'page/page_detail.html'

    def get_object(self, queryset=None):
        return Page.objects.get(url=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(PageDetail, self).get_context_data(**kwargs)
        current_url = self.request.path
        context['seo'] = SeoPage.objects.get(slug=current_url)
        return context
