from django.urls import path

from . import views

urlpatterns = [
    path('jewels/', views.index),
]
