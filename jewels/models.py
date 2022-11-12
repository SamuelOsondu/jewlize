import uuid

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name}'


class Item(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    item_amount = models.FloatField(max_length=20)
    item_img = models.ImageField(upload_to='images')

    def __str__(self):
        return f'{self.name} - {self.slug}'


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

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


#
# class Category(models.Model):
#     name = models.CharField(max_length=50)
#
#     @staticmethod
#     def get_all_categories():
#         return Category.objects.all()
#
#     def __str__(self):
#         return self.name
#

#
# class Products(models.Model):
#     name = models.CharField(max_length=60)
#     price = models.IntegerField(default=0)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
#     description = models.CharField(
#         max_length=250, default='', blank=True, null=True)
#     image = models.ImageField(upload_to='uploads/products/')
#
#     @staticmethod
#     def get_products_by_id(ids):
#         return Products.objects.filter(id__in=ids)
#
#     @staticmethod
#     def get_all_products():
#         return Products.objects.all()
#
#     @staticmethod
#     def get_all_products_by_categoryid(category_id):
#         if category_id:
#             return Products.objects.filter(category=category_id)
#         else:
#             return Products.get_all_products()
#
#

