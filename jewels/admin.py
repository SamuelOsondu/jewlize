from django.contrib import admin

from .models import Item

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Item, ItemAdmin)
