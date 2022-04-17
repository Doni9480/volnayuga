from .models import StaticData

def data(request):
    data = StaticData.objects.first()
    context = {
        'logo': data.logo,
        'logo_footer':data.logo_footer,
        'phone':data.phone,
        'email':data.email,
        'banner':data.banner,
    }
    return context


