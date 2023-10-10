from django.contrib import admin
from shop.models import Product, Order, Cart

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'price', 'quantity')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'ordered')

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered')

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)