from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'price', 'weight', 'in_stock', 'created_at')
    list_filter   = ('in_stock', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('in_stock',)
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        obj.save(using='products_db')
