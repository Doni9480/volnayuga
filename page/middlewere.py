from django.shortcuts import render
from page.models import Page

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            try:
                context = {
                        "object": Page.objects.get(url='404')
                }
            except Exception:
                context = {
                        "object": {
                            'title': "Страница не найдено!",
                            'content': "Страница не найдено!\n(Можно изменить в админке)",
                        }
                }
            return render(request, '404.html', context=context, status=404)

        return response