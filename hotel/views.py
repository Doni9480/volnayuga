from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

from accounts.models import MyUser
from review.models import Review
from .models import Hotel, BookmarkHotel
from region.models import Region
import json

from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.views import View


def home_view(request):
    region_list = Region.objects.filter(parent=None)
    review_list = Review.objects.filter(verificated=True)
    region_popular_list = Region.objects.filter(is_popular=True)
    context = {
        'region_list': region_list,
        'region_popular_list': region_popular_list,
        'review_list': review_list,
    }
    return render(request, template_name='hotel/home.html', context=context)


class BookmarkView(View):
    # в данную переменную будет устанавливаться модель закладок, которую необходимо обработать
    model = BookmarkHotel

    def post(self, request, pk):
        # when the user is unauthenticated, before calling a method that takes request as a parameter do:
        if request.user.is_anonymous:
            # нам потребуется пользователь
            anonUser, created = MyUser.objects.get_or_create(email="anonuser@anon.ru", phone='111111111')
            print(anonUser, created)
            user = MyUser.objects.get(id=anonUser.id)
        else:
            user = auth.get_user(request)
        # пытаемся получить закладку из таблицы, или создать новую
        bookmark, created = self.model.objects.get_or_create(user=user, hotel_id=pk)
        # если не была создана новая закладка,
        # то считаем, что запрос был на удаление закладки
        if not created:
            bookmark.delete()

        return HttpResponse(
            json.dumps({
                "result": created,
                "count": self.model.objects.filter(hotel_id=pk).count()
            }),
            content_type="application/json"
        )


def favorites_list(request):
    favorites_list = []
    if request.session.get('favorites'):
        favorites_list_ids = request.session.get('favorites')
        for item in favorites_list_ids:
            favorites_list.append(Hotel.objects.get(id=item))
    else:
        favorites_list_ids = []
    context = {
        'favorite_list': favorites_list,
        'favorite_list_ids': favorites_list_ids,
    }
    return render(request, 'hotel/bookmarks.html', context)


def add_to_favorites(request, id):
    if request.is_ajax() and request.method == 'POST':
        if not request.session.get('favorites'):
            request.session['favorites'] = list()
        else:
            request.session['favorites'] = list(request.session['favorites'])

        if id not in request.session['favorites']:
            request.session['favorites'].append(id)
            request.session.modified = True
            message = 1
            return JsonResponse(status=200, data={'status': 'true', 'message': message})

        else:
            request.session['favorites'].remove(id)
            request.session.modified = True
            message = 2
            return JsonResponse(status=200, data={'id': id, 'message': message})
    return JsonResponse(status=400, data={'id': id, 'message': 'Что то пошло не так!'})


def remove_from_favorites(request, id):
    if request.method == 'POST':
        for item in request.session['favorites']:
            if item['id'] == id:
                item.clear()
    if not request.session['favorites']:
        del request.session['favorites']

    request.session.modified = True
    return redirect(request.POST.get('url_form'))
