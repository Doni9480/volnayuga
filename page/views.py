from django.shortcuts import render
from django.views.generic import DetailView
from page.models import Page


class PageDetail(DetailView):
    model = Page
    template_name = 'page/page_detail.html'

    def get_object(self, queryset=None):
        return Page.objects.get(url=self.kwargs['slug'])
