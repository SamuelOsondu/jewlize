from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json

from .models import Item, Cart, Customer
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth import login, authenticate, logout  # add this
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages


# Create your views here.

def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save(commit=True)
			user.save()
			Customer.objects.create(
				user=user,
				name=user.username,
				email=user.email
			)
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("jewels:index.html")
		messages.error(request, form.errors)
	form = NewUserForm()
	return render(request, "jewels/register.html", {"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return HttpResponseRedirect('/jewels')
			else:
				messages.error(request, form.errors)
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request, 'jewels/login.html', context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("/jewels")


def index(request):
	items = Item.objects.all()
	return render(request, 'jewels/index.html', {'items': items, 'logged_in': request.user.is_authenticated})


@login_required(login_url='login')
def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		cart, created = Cart.objects.get_or_create(customer=customer, completed=False)
		cartitem = cart.cartitem_set.all()
	else:
		cartitem = []
		cart = {"get_cart_total": 0, "get_itemtotal": 0}

	return render(request, 'jewels/cart.html', {'cartitem': cartitem, 'cart': cart})


def contact(request):
	return render(request, 'jewels/contact.html')


def jewellery(request):
	items = Item.objects.all()
	return render(request, 'jewels/jewellery.html', {'items': items})


def update_item(request):
	data = json.loads(request.data)
	productId = data['productId']
	action = data['action']

	print('Action:', action)
	print('productId:', productId)

	customer = request.user.customer
	item = Item.objects.get(id=productId)
	cart, created = Cart.objects.get_or_create(customer=customer, completed=False)

	cartitem, created = Item.objects.get_or_create(cart=cart, item=item)

	if action == 'add':
		cartitem.quantity = (cartitem.quantity + 1)
	elif action == 'remove':
		cartitem.quantity = (cartitem.quantity - 1)
	cartitem.save()

	if cartitem.quuantity <= 0:
		cartitem.delete()
		
	return JsonResponse('Item was added', safe=False)
