from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('jewellery/', views.jewellery, name='jewellery'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_request, name='login'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart, name="cart"),
    path('logout/', views.logout_request, name="logout"),
    path('update_item/', views.update_item, name="update_item"),
]
