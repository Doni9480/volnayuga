from page.models import Page
from .models import StaticData

def data(request):
    if StaticData.objects.first():
        data = StaticData.objects.first()
        context = {
            'logo': data.logo,
            'logo_footer':data.logo_footer,
            'phone':data.phone,
            'email':data.email,
            'banner':data.banner,
        }
    else:
        context = {
            'logo': None,
            'logo_footer': None,
            'phone': None,
            'email': None,
            'banner': None,
        }
    return context


def page(request):
    context = {'page_list': Page.objects.all()}
    return context


