from django.shortcuts import render
from .models import Item
# Create your views here.


def index(request):
    items = Item.objects.all()

    return render(request, 'jewels/index.html', {'user': items})


def about(request):
    return render(request, 'jewels/about.html')


def contact(request):
    return render(request, 'jewels/contact.html')


def jewellery(request):
    items = Item.objects.all()
    return render(request, 'jewels/jewellery.html', {'items': items})

def login(request):
    return render(request, 'jewels/login.html')


def register(request):
    return render(request, 'jewels/register.html')
