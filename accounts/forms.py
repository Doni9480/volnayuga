import form as form
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, HTML, Row, Column, ButtonHolder, Div, Field, MultiField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, CheckboxSelectMultiple
from django.urls import reverse

from hotel.models import *


# Create your forms here.

class NewUserForm(UserCreationForm):
    """Регистрация пользователя"""
    email = forms.EmailField(required=True)

    class Meta:
        model = MyUser
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class HotelUpdateForm(forms.ModelForm):
    """Обновление информации о гостинице"""

    class Meta:
        model = Hotel
        fields = '__all__'
        exclude = ['user', 'meta_title', 'meta_description', 'object_type', 'chek_in', 'chek_out', 'prepayment',
                   'prepayments_term',
                   'requisites', 'early_booking_discount', 'minimum', 'child',
                   'pets', 'free_cancel', 'another_rules', 'options']


class HotelRulesForm(forms.ModelForm):
    """Добавляем правила к гостинице"""

    class Meta:
        model = Hotel
        fields = ['chek_in', 'chek_out', 'prepayment', 'prepayments_term',
                  'requisites', 'early_booking_discount', 'minimum', 'child',
                  'pets', 'free_cancel', 'another_rules']


class HotelFilterForm(forms.ModelForm):
    """Фильтр отелей"""
    options_food = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                  queryset=HotelOption.objects.filter(category='food'), required=False)
    options_service = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                     queryset=HotelOption.objects.filter(category='service'),
                                                     required=False)
    options_booking = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                     queryset=HotelOption.objects.filter(category='booking'),
                                                     required=False)
    beach = forms.MultipleChoiceField(choices=BEACHCHOICE, widget=forms.CheckboxSelectMultiple(), required=False)
    remoteness = forms.MultipleChoiceField(choices=BEACHREMOTENESS, widget=forms.CheckboxSelectMultiple(), required=False)

    price_min = forms.DecimalField(required=False)
    price_max = forms.DecimalField(required=False)

    class Meta:
        model = Hotel
        fields = ['options_food', 'options_service', 'options_booking', 'object_type', 'beach', 'remoteness']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            Div(
                HTML("""<p>Цена за номер, руб.</p>"""),
                Div(
                    Div(
                        'price_min',
                        HTML("""<p>-</p>"""),
                        'price_max',

                        css_class='input-cont flex juatifyBetween alignCenter',
                    ),

                    css_class='rangeSlider',
                ),
                css_class='left-filter1',
            ),
        Div(
            HTML("""<p>Питание</p>"""),
            'options_food',
            css_class='left-filter2'

        ),
        Div(
            HTML("""<p>Удобства</p>"""),
            'options_service',
            css_class='left-filter2'

        ),
        Div(
            HTML("""<p>Бронирование</p>"""),
            'options_booking',
            css_class='left-filter2'
        ),
        Div(
            HTML("""<p>Пляж</p>"""),
            'beach',
            css_class='left-filter2',
        ),
        Div(
            HTML("""<p>Расстояние до моря</p>"""),
            'remoteness',
            css_class='left-filter2',
        ),
        ButtonHolder(
            Submit('submit', 'Показать', css_class='button')
        )


        )


class HotelOptionForm(forms.ModelForm):
    """Добавляем опции к гостинице"""
    options = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                  queryset=HotelOption.objects.all(), required=False)


    class Meta:
        model = Hotel
        fields = ['options']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False



class NumberCreateForm(forms.ModelForm):
    options = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=NumberOption.objects.all(),
                                             label='Опции')
    """Добавление номеров к гостинице """

    # image = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}), required=False, label='Изображения')
    class Meta:
        model = Number
        fields = '__all__'
        exclude = ['hotel']


class ContactForm(forms.ModelForm):
    """Форма для добавления и редактирования контактов гостиницы"""

    class Meta:
        model = HotelContact
        fields = '__all__'
        exclude = ['hotel']


class DistanceForm(forms.ModelForm):
    """"""

    class Meta:
        model = DistanceTime
        fields = '__all__'


class DistanceTimeForm(forms.ModelForm):
    """"""
    time = forms.IntegerField(max_value=999, label='В минутах')

    class Meta:
        model = DistanceTime
        fields = '__all__'
        exclude = ['hotel']
