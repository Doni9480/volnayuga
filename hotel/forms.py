from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, ButtonHolder, Submit
from django import forms
from django.forms import HiddenInput
from django.urls import reverse

from hotel.models import HotelOption, Hotel, BEACHCHOICE, BEACHREMOTENESS

import django_filters



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
        self.helper.form_action = reverse('region:hotel_filter_left', kwargs={'slug': 'tuapse'})
        self.helper.layout = Layout(
            Div(
                HTML("""<p>Цена за номер, руб.</p>"""),
                Div(
                    Div(
                        HTML("""<input type="text" class="range_min light left">"""),
                        HTML("""<div>-</div>"""),
                        HTML("""<input type="text" class="range_max light right">"""),

                        css_class='input-cont flex juatifyBetween alignCenter',
                    ),
                    HTML("""<input class="min" name="range_1" type="range" min="1" max="100" value="10">
                    <input class="max" name="range_2" type="range" min="1" max="100" value="90">"""
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

class HotelFilter(django_filters.FilterSet):


    class Meta:
        model = Hotel
        form = HotelFilterForm
        fields = ['options', 'object_type', 'beach', 'remoteness']







