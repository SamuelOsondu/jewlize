from django.shortcuts import render
from .models import Item
# Create your views here.

from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth import login, authenticate, logout  # add this
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("jewels/index.html")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="jewels/register.html", context={"register_form":form})


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
				return redirect("/jewels")
			else:
				messages.error(request,"Invalid username or password.")
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
	return render(request, 'jewels/index.html', {'user': items})


def about(request):
	return render(request, 'jewels/about.html')


def contact(request):
	return render(request, 'jewels/contact.html')


def jewellery(request):
	items = Item.objects.all()
	return render(request, 'jewels/jewellery.html', {'items': items})





# def register(request):
#     return render(request, 'jewels/register.html')
