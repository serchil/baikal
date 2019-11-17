from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Tour
from .models import User
class TourForm(forms.ModelForm):
    class Meta:
            model = Tour
            fields = ['id', 'name', 'url', 'description', 'slider',  'number_of_days', 'min_price',  'places', 'preview_descr', 'preview_img', 'activity_status',  'show_on_main_status']
            labels = {
            'name': _('Название тура'), 'url': _('url'), 'description': _('Описание'), 'number_of_days': ('Количество дней'), 'slider':('Изображения слайдера'),'places':('Направления'), 'min_price': ('Стоимость'), 'preview_descr': ('Описание превью'), 'preview_img': ('Изображение для превью'), 'activity_status': ('Активен'), 'show_on_main_status': ('Отображать на главной')
        }


class UserForm(forms.ModelForm):
    class Meta:
            model = User
            fields = ['id', 'name',  'surname', 'email',  'phone_number', 'password', 'password']
            labels = {
            'name': _('Имя'), 'surname': _('Фамилия'), 'email': _('E-mail'), 'phone_number': ('Номер телефона'), 'password': ('Пароль'), 'password': ('Пароль')
            }
