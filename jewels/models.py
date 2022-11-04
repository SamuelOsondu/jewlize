from django.db import models

# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    item_amount = models.CharField(max_length=20)
    item_img = models.ImageField(upload_to='images')

    def __str__(self):
        return f'{self.name} - {self.slug}'

