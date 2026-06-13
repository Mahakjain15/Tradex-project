from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = ['name', 'weight', 'price', 'description', 'image', 'in_stock']
        widgets = {
            'name':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'weight':      forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'placeholder': 'kg'}),
            'price':       forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '₹'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image':       forms.FileInput(attrs={'class': 'form-control'}),
            'in_stock':    forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
