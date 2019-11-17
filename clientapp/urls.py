from django.urls import path
from . import views
from django.conf.urls import url
from django.views.generic.base import TemplateView
app_name = 'clientapp'
urlpatterns = [
        path('baikal/', views.index, name = "index"),


]
