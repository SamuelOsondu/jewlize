from django.contrib import admin

from .models import *

# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Item)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ShippingAddress)

