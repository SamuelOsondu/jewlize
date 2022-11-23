from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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
			return redirect(reverse("jewels:index.html"))
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
		cart, created = Cart.object.get_or_create(customer=customer, completed=False)
		cart_items = cart.cartitem_set.all()
		return render(request, 'jewels/cart.html', {'cart_items': cart_items})


def contact(request):
	return render(request, 'jewels/contact.html')


def jewellery(request):
	items = Item.objects.all()
	return render(request, 'jewels/jewellery.html', {'items': items})

