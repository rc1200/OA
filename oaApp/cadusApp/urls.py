from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('super', views.super, name='super'),
]
