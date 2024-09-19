from django.urls import path
from . import views

urlpatterns = [
    path('DigitalHome/', views.home, name='DigitalHome'),
    path('device/inputprompt', views.inputprompt, name='inputprompt'),
    path('device/inputis', views.inputis, name='inputis'),

]