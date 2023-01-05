from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json

from .models import Item, Cart, Customer, CartItem
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth import login, authenticate, logout  # add this
from django.shortcuts import render, redirect
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
            messages.success(request, "Registration successful.")
            return redirect("jewels:index.html")
        messages.error(request, form.errors)
    form = NewUserForm()
    return render(request, "jewels/register.html", {"register_form": form})


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
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'jewels/login.html', context={"login_form": form})


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


from django.shortcuts import HttpResponseRedirect

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        product = Item.objects.get(id=product_id)
    except Item.DoesNotExist:
        messages.error(request, 'Product does not exist')
        return redirect('product_list')

    try:
        cart_entry = Cart.objects.get(user=request.user, product=product)
        cart_entry.quantity += 1
        cart_entry.save()
    except Cart.DoesNotExist:
        Cart.objects.create(user=request.user, product=product, quantity=1)

    messages.success(request, 'Product added to cart')

    next = request.POST.get('next', request.GET.get('next'))
    if next:
        return redirect(next)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def update_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        product = Item.objects.get(id=product_id)
    except Item.DoesNotExist:
        messages.error(request, 'Product does not exist')
        return redirect('view_cart')

    try:
        cart_entry = Cart.objects.get(user=request.user, product=product)
    except Cart.DoesNotExist:
        messages.error(request, 'Product not in cart')
        return redirect('view_cart')

    cart_entry.quantity = request.POST['quantity']
    cart_entry.save()

    return redirect('view_cart')


def delete_from_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        product = Item.objects.get(id=product_id)
    except Item.DoesNotExist:
        messages.error(request, 'Product does not exist')
        return redirect('view_cart')

    try:
        cart_entry = Cart.objects.get(user=request.user, product=product)
    except Cart.DoesNotExist:
        messages.error(request, 'Product not in cart')
        return redirect('view_cart')

    cart_entry.delete()

    return redirect('view_cart')


