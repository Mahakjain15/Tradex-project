from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product
from .forms import ProductForm


def product_list(request):
    query    = request.GET.get('q', '')
    products = Product.objects.using('products_db').all()
    if query:
        products = products.filter(name__icontains=query)
    paginator = Paginator(products, 12)
    page_obj  = paginator.get_page(request.GET.get('page'))
    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'query': query,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.using('products_db'), pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save(using='products_db')
            messages.success(request, f'Product "{product.name}" added!')
            return redirect('products:list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Add Product'})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product.objects.using('products_db'), pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated!')
            return redirect('products:detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Edit Product', 'product': product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product.objects.using('products_db'), pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
        return redirect('products:list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})
