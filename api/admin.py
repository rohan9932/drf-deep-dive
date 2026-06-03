from django.contrib import admin
from . import models

admin.site.site_header = "Shop Admin"
admin.site.index_title = "Shop Admin Title"

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline, # attaching OrderItem obj in Order page
    ] 

admin.site.register(models.Order, OrderAdmin)