from django.shortcuts import render
from django.views.generic import DetailView
from page.models import Page
from seo.models import SeoPage
from page.models import StatusCode


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


def handler404(request, exception=None, template_name='404.html'):
    try:
        context = {
            "object": StatusCode.objects.get(pk=1)
        }
    except Exception:
        context = {
            "object": {
                'title': "Страница не найдено!",
                'h1': "Страница не найдено!",
                'content_1': "Страница не найдено!\n(Можно изменить в админке)",
            }
        }
    return render(request=request, template_name=template_name, context=context, status=404)
