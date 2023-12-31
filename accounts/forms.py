import form as form
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, HTML, Row, Column, ButtonHolder, Div, Field, MultiField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, CheckboxSelectMultiple, modelformset_factory, widgets
from django.urls import reverse
from hotel.models import *



class HotelUpdateForm(forms.ModelForm):
    """Обновление информации о гостинице"""

    class Meta:
        model = Hotel
        fields = '__all__'
        exclude = ['user', 'meta_title', 'meta_description', 'object_type', 'chek_in', 'chek_out', 'prepayment',
                   'prepayments_term',
                   'requisites', 'early_booking_discount', 'minimum', 'child',
                   'pets', 'free_cancel', 'another_rules', 'options', 'distance','premium']


class HotelRulesForm(forms.ModelForm):
    """Добавляем правила к гостинице"""

    class Meta:
        model = Hotel
        fields = ['chek_in', 'chek_out', 'prepayment', 'prepayments_term',
                  'requisites', 'early_booking_discount', 'minimum', 'child',
                  'pets', 'free_cancel', 'another_rules']


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


class HotelPricePeriodForm(forms.ModelForm):
    start = forms.DateField(label="Начало периода",
                            widget=widgets.DateInput(attrs={'class':'datepicker'}))
    end = forms.DateField(label="Конец периода",
                          widget=widgets.DateInput(attrs={'class':'datepicker'}))

    class Meta:
        model = PricePeriod
        fields = ('start', 'end')


PricePeriodFormset = modelformset_factory(PricePeriod, form=HotelPricePeriodForm, fields=('start','end' ), extra=12)
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
        fields = ['distance', 'method', 'time']

    def __init__(self, *args, **kwargs):
        hotel = kwargs.pop('hotel')
        distance_id_exclude = Distance.objects.filter(hotel=hotel)
        super(DistanceForm, self).__init__(*args, **kwargs)
        self.fields['distance'].queryset = Distance.objects.all().exclude(hotel=hotel)


class DistanceTimeForm(forms.ModelForm):
    """"""
    time = forms.IntegerField(max_value=999, label='В минутах')

    class Meta:
        model = DistanceTime
        fields = '__all__'
        exclude = ['hotel']

