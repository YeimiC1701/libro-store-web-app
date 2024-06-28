from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('masLeidos/', views.masLeidos, name='masLeidos'),
]