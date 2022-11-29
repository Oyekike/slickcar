from django.contrib import admin
from home.models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('brand',)}
    list_display = ['id', 'brand', 'description', 'pix', 'slug']

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['id', 'type', 'name', 'color', 'price', 'registered', 'uploaded_at']

class ContactAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'email', 'message', 'sent']

admin.site.register(AppInfo)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact, ContactAdmin)
