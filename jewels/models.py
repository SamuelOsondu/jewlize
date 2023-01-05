import uuid

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                related_name="customer"
                                )
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    item_amount = models.FloatField(max_length=20)
    item_img = models.ImageField(upload_to='images')

    def __str__(self):
        return f'{self.name} - {self.slug}'


# class Cart(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     cart_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
#     completed = models.BooleanField(default=False)
#
#     @property
#     def get_cart_total(self):
#         cart_items = self.cartitem_set.all()
#         total = sum([item.get_total for item in cart_items])
#         return total
#
#     def __str__(self):
#         return f'{self.id}'
#

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

    def __str__(self):
        return f'{self.item.name}'


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.address}'

