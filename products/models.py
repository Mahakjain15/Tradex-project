from django.db import models


class Product(models.Model):
    name       = models.CharField(max_length=200)
    weight     = models.DecimalField(max_digits=10, decimal_places=3, help_text='Weight in kilograms')
    price      = models.DecimalField(max_digits=12, decimal_places=2, help_text='Price in INR')
    description = models.TextField(blank=True, default='')
    image      = models.ImageField(upload_to='products/', blank=True, null=True)
    in_stock   = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — ₹{self.price}'
