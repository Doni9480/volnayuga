from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, ButtonHolder, Submit
from django import forms
from django.core.validators import validate_image_file_extension
from django.forms import HiddenInput
from django.urls import reverse

from hotel.models import HotelOption, Hotel, BEACHCHOICE, BEACHREMOTENESS, TypeofObject, HotelPhoto

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
    object_type = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                            queryset=TypeofObject.objects.all(),
                                            required=False)
    beach = forms.MultipleChoiceField(choices=BEACHCHOICE, widget=forms.CheckboxSelectMultiple(), required=False)
    remoteness = forms.MultipleChoiceField(choices=BEACHREMOTENESS, widget=forms.CheckboxSelectMultiple(), required=False)

    price_min = forms.DecimalField(required=False)
    price_max = forms.DecimalField(required=False)



    class Meta:
        model = Hotel
        fields = ['city','object_type','options_food', 'options_service', 'options_booking', 'object_type', 'beach', 'remoteness']

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
                        HTML("""<input type="text" class="range_min light left">"""),
                        HTML("""<div>-</div>"""),
                        HTML("""<input type="text" class="range_max light right">"""),

                        css_class='input-cont flex juatifyBetween alignCenter',
                    ),
                    HTML("""<input class="min" name="range_1" type="range" min="1" max="100" value="0">
                    <input class="max" name="range_2" type="range" min="1" max="100" value="100">"""
                    ),
                    css_class='rangeSlider',
                ),
                css_class='left-filter1',
            ),
        Div(
            HTML("""<p>Тип жилья</p>"""),
            'object_type',
            css_class='left-filter2'
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
        fields = ['object_type', 'options', 'object_type', 'beach', 'remoteness']


class HotelAdminForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'

    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        label= 'Добавить фото',
        required=False,
    )

    def clean_photos(self):
        """Make sure only images can be uploaded."""
        for upload in self.files.getlist("images"):
            validate_image_file_extension(upload)

    def save_photos(self, hotel):
        """Process each uploaded image."""
        for upload in self.files.getlist("images"):
            images = HotelPhoto(hotel=hotel, image=upload)
            images.save()







