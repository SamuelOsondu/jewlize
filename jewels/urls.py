from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('jewellery/', views.jewellery, name='jewellery'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_request, name='login'),
    path('register/', views.register, name='register'),
    path("logout", views.logout_request, name="logout"),
]
