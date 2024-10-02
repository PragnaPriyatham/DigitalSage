from django.urls import path
from . import views
from .views import DeviceList

urlpatterns = [
    path('DigitalHome/', views.home, name='DigitalHome'),
    path('device/inputprompt', views.inputprompt, name='inputprompt'),
    path('device/inputis', views.inputis, name='inputis'),
    path('device/divlist', DeviceList.as_view(), name='divlist'),

]