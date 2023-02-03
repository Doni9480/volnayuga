from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.functional import lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormMixin

from review.models import Review
from .forms import *
from hotel.models import *
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.forms import PasswordResetForm
from .models import MyUser
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.forms import formset_factory


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация завершена.")
            return redirect('/accounts/lk', )
        messages.error(request, "Регистрация не прошла.")
    form = NewUserForm()
    return render(request=request, template_name="accounts/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы вошли как {email}.")
                return redirect('/accounts/lk', )
            else:
                messages.error(request, "Неверный логин или пароль.")
        else:
            messages.error(request, "Неверный логин или пароль.")
    form = AuthenticationForm()
    return render(request=request, template_name="accounts/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Вы успешно вышли.")
    return redirect('/accounts/lk', )


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = MyUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'justscoundrel@yandex.ru', [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/password_reset.html",
                  context={"password_reset_form": password_reset_form})


@method_decorator(login_required, name='dispatch')
class HotelList(ListView):
    """Список отелей владельца"""
    model = Hotel
    template_name = 'accounts/lk_home.html'

    def get_queryset(self):
        return Hotel.objects.filter(user=self.request.user)


class HotelDetail(FormMixin, DetailView):
    """Страница отображения всех взаимосвязных моделей гостиницы"""
    model = Hotel
    form_class = HotelRulesForm
    template_name = 'accounts/lk_hotel_detail.html'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(HotelDetail, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return self.get_queryset().filter(id=self.kwargs['pk']).get()

    def get_context_data(self, **kwargs):
        context = super(HotelDetail, self).get_context_data(**kwargs)
        context['form'] = HotelRulesForm(instance=self.object)
        period_list = PricePeriod.objects.filter(hotel=self.object)
        number_list = Number.objects.filter(hotel=self.object)
        price_list = Price.objects.filter(number__in=number_list)
        data = {"price": [], "period": [], "number": []}
        for price in price_list:
            data['price'].append(price.price)
            data['period'].append(price.period)
            data['number'].append(price.number)
        context['data'] = data
        context['price_list'] = price_list

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = HotelRulesForm(instance=self.object, data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        rule = form.save(commit=False)
        rule = self.object
        form.save()
        return super(HotelDetail, self).form_valid(form)

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class HotelRules(UpdateView):
    """Добавление правил гостиниы"""
    model = Hotel
    form_class = HotelRulesForm
    template_name = 'accounts/lk_hotel_rules.html'

    def get_object(self, queryset=None):
        obj = super(HotelRules, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return self.get_queryset().filter(id=self.kwargs['pk']).get()

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.hotel = self.get_queryset().filter(id=self.kwargs['pk']).get()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.id})


class HotelCreate(CreateView):
    """Создание гостиницы"""
    model = Hotel
    template_name = 'accounts/lk_hotel_create.html'
    fields = ['title', 'object_type', 'address', 'city', 'remoteness', 'beach']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.id})


class HotelUpdate(UpdateView):
    """Обновляем инфу о гостинице"""
    model = Hotel
    template_name = 'accounts/lk_hotel_update.html'
    form_class = HotelUpdateForm

    def get_object(self, queryset=None):
        obj = super(HotelUpdate, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return self.get_queryset().filter(id=self.kwargs['pk']).get()

    def form_valid(self, form):
        self.object.save()
        for key in form.files:
            img_files = form.files.getlist(key)
            for file in img_files:
                HotelPhoto.objects.create(image=file, hotel=self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.id})


class HotelPhotoDelete(DeleteView):
    """"""
    model = HotelPhoto
    template_name = 'accounts/lk_hotel_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(HotelPhotoDelete, self).get_object()
        if not obj.hotel.user == self.request.user:
            raise Http404
        return self.get_object().filter(id=self.kwargs['photo_pk']).get()

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.hotel.id})


class HotelOptionUpdate(UpdateView):
    """Обновляем опции к гостинице"""
    model = Hotel
    form_class = HotelOptionForm
    template_name = 'accounts/lk_hotel_options_add.html'

    def get_object(self, queryset=None):
        obj = self.get_queryset().filter(id=self.kwargs['hotel_pk']).get()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.id})


class HotelDelete(DeleteView):
    """Удаляем гостиницу"""
    model = Hotel
    template_name = "accounts/lk_hotel_confirm_delete.html"

    def get_object(self, queryset=None):
        obj = super(HotelDelete, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return self.get_queryset().filter(id=self.kwargs['pk']).get()

    def get_success_url(self):
        return reverse('accounts:user_hotel_list')


class HotelPricePeriod(CreateView):
    """Создание ценового периода гостиницы"""
    model = PricePeriod
    template_name = "accounts/lk_hotel_priceperiod.html"

    def get_object(self, queryset=None):
        obj = super(HotelPricePeriod, self).get_object()
        return self.get_queryset().filter(id=self.kwargs['pk']).get()

    def get_success_url(self):
        return reverse('accounts:user_hotel_list')


class HotelPricePeriodUpdate(UpdateView):
    """Редактирование ценового периода гостиницы"""
    model = Hotel
    template_name = "accounts/lk_hotel_priceperiod.html"
    form_class = HotelPricePeriodForm

    def get_context_data(self, **kwargs):
        context = super(HotelPricePeriodUpdate, self).get_context_data(**kwargs)
        context['formset'] = PricePeriodFormset(queryset=PricePeriod.objects.filter(hotel__id=self.kwargs['pk']))
        return context

    def post(self, request, *args, **kwargs):
        formset = PricePeriodFormset(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.hotel = Hotel.objects.get(id=self.kwargs['pk'])
            instance.save()
        return redirect(reverse('accounts:user_hotel_price_period_update', kwargs={'pk': self.kwargs['pk']}))

    def form_invalid(self, formset):
        return self.render_to_response(self.get_context_data(formset=formset))

    def get_success_url(self):
        return reverse('accounts:user_hotel_price_period_update', kwargs={'pk': self.object.id})


def price_period_delete(request, pk):
    """Удаление периода цен"""
    if request.is_ajax() or request.method == 'POST':
        price_period = PricePeriod.objects.get(id=pk)
        price_period.delete()
        return JsonResponse({'post': 'true'})
    return JsonResponse({'post': 'false'})


def price_update(request):
    """Апдейт цен в номерах"""
    if request.is_ajax() or request.method == 'POST':
        period = PricePeriod.objects.get(id=request.POST['period'])
        number = Number.objects.get(id=request.POST['number'])
        price = request.POST['price']
        if 'is_extra' in request.POST and 'price-id' in request.POST:
            print('extra')
            price_object = Price.objects.get(id=request.POST['price-id'])
            price_object.extra_bed = price
            price_object.save()
        elif 'price-id' in request.POST:
            print('update')
            price_object = Price.objects.get(id=request.POST['price-id'])
            price_object.price = price
            price_object.save()
        else:
            Price.objects.create(number=number, period=period, price=price)
            print('create')
        return JsonResponse({'post': 'true'})
    return JsonResponse({'post': 'false'})


def hotel_image_upload(request, pk):
    """Добавление изображений закладке фотографии гостиницы"""
    if request.method == 'POST':
        my_file = request.FILES.get('file')
        hotel = Hotel.objects.get(id=pk)
        HotelPhoto.objects.create(image=my_file, hotel=hotel)
        return JsonResponse({'post': 'true'})
    return JsonResponse({'post': 'false'})


def hotel_image_delete(request, pk):
    """Удаление изображений в закладке фотографии гостиницы"""
    if request.method == 'POST':
        photo = HotelPhoto.objects.get(id=pk)
        photo.delete()
        return JsonResponse({'post': 'true'})
    return JsonResponse({'post': 'false'})


class NumberCreate(CreateView):
    """Добавялем номер к гостинице"""
    model = Number
    template_name = 'accounts/lk_number_create.html'
    form_class = NumberCreateForm

    def form_valid(self, form):
        form.save(commit=False)
        hotel = Hotel.objects.get(id=self.kwargs['hotel_pk'])
        form.instance.hotel = hotel

        for key in form.files:
            img_files = form.files.getlist(key)
            for file in img_files:
                NumberPhoto.objects.create(image=file, number=self.object)

        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.hotel.id})


class NumberUpdate(UpdateView):
    """Обновляем инфу о номере"""
    model = Number
    template_name = 'accounts/lk_number_update.html'
    form_class = NumberCreateForm

    def get_object(self, queryset=None):
        obj = super(NumberUpdate, self).get_object()
        if not obj.hotel.user == self.request.user:
            raise Http404
        return self.get_queryset().filter(id=self.kwargs['pk']).get()

    def form_valid(self, form):
        if form.is_valid():
            form.save(commit=False)
            for key in form.files:
                img_files = form.files.getlist(key)
                for file in img_files:
                    NumberPhoto.objects.create(image=file, number=self.object)

            form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.hotel.id})


def number_image_upload(request, pk):
    """Добавление изображений к номеру через дропбокс"""
    if request.method == 'POST':
        my_file = request.FILES.get('file')
        number = Number.objects.get(id=pk)
        NumberPhoto.objects.create(image=my_file, number=number)
        return JsonResponse({'post': 'true'})
    return JsonResponse({'post': 'false'})


class NumberPhotoDelete(DeleteView):
    """"""
    model = NumberPhoto
    template_name = 'accounts/lk_hotel_confirm_delete.html'

    def get_object(self, queryset=None):
        pk = self.kwargs['photo_pk']
        return self.get_queryset().filter(id=pk).get()

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.number.hotel.id})


def number_image_delete(request, image_pk):
    """Удаление изображений номера"""
    if request.method == 'POST':
        photo = NumberPhoto.objects.get(id=image_pk)
        photo.delete()
        return JsonResponse({'post': 'true'})
    return JsonResponse({'post': 'false'})


class NumberDelete(DeleteView):
    """Удаляем номер"""
    model = Number
    template_name = "accounts/lk_hotel_confirm_delete.html"

    def get_object(self, queryset=None):
        obj = super(NumberDelete, self).get_object()
        if not obj.hotel.user == self.request.user:
            raise Http404
        return self.get_queryset().filter(id=self.kwargs['pk']).get()

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.hotel.id})


class ContactCreate(CreateView):
    """Добавялем контакты к гостинице"""
    model = Hotel
    template_name = 'accounts/lk_contact_create.html'
    form_class = ContactForm

    def form_valid(self, form):
        form.save(commit=False)
        hotel = Hotel.objects.get(id=self.kwargs['hotel_pk'])
        form.instance.hotel = hotel
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.hotel.id})


class ContactUpdate(UpdateView):
    """"""
    model = HotelContact
    template_name = 'accounts/lk_contact_create.html'
    form_class = ContactForm

    def get_object(self, queryset=None):
        return self.get_queryset().filter(id=self.kwargs['pk']).get()

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.hotel.id})


class ContactDelete(DeleteView):
    """Удаляем контакт"""
    model = HotelContact
    template_name = "accounts/lk_hotel_confirm_delete.html"

    def get_object(self, queryset=None):
        obj = super(ContactDelete, self).get_object()
        if not obj.hotel.user == self.request.user:
            raise Http404
        return self.get_queryset().filter(id=self.kwargs['pk']).get()

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.hotel.id})


class DistanceAdd(CreateView):
    """"Create Distance"""
    model = Distance
    form_class = DistanceForm
    template_name = 'accounts/lk_hotel_distance_add.html'

    def get_form_kwargs(self):
        kwargs = super(DistanceAdd, self).get_form_kwargs()
        hotel = Hotel.objects.get(id=self.kwargs['hotel_pk'])
        kwargs['hotel'] = hotel
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        hotel = Hotel.objects.get(id=self.kwargs['hotel_pk'])
        self.object.hotel = hotel
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.hotel.id})


class DistanceDelete(DeleteView):
    """Distance delete"""
    model = DistanceTime
    template_name = "accounts/lk_hotel_confirm_delete.html"

    def get_object(self, queryset=None):
        return self.get_queryset().filter(id=self.kwargs['pk']).get()

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.kwargs['hotel_pk']})


class DistanceUpdate(FormMixin, DetailView):
    """Distance update"""
    model = Hotel
    form_class = DistanceForm
    second_form_class = DistanceTimeForm
    template_name = 'accounts/lk_hotel_distance.html'

    def get_object(self, queryset=None):
        obj = self.get_queryset().filter(id=self.kwargs['hotel_pk']).get()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super(DistanceUpdate, self).get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        context['form2'] = self.second_form_class(self.request.GET)
        context['distance_list'] = Distance.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = DistanceForm(instance=self.object, data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save(commit=False)
        form.hotel.id = self.kwargs['hotel_pk']
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accounts:user_hotel_detail', kwargs={'pk': self.object.id})


class HotelReviewList(ListView):
    """LK Hotel Review`s list"""
    model = Review
    template_name = 'accounts/lk_hotel_review.html'
    context_object_name = 'review_list'

    def get_queryset(self):
        return HotelReview.objects.filter(hotel__user=self.request.user)


class HotelHelp(TemplateView):
    """Lk Hotel help page"""
    template_name = 'accounts/lk_hotel_help.html'
