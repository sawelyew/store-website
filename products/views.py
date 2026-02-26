from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, ProductCategory

# Create your views here.
def index(request):
    context = {'title': 'Home Page'}
    return render(request, 'products/index.html', context)

def products(request, category_id=None):
    sizes = ['XS', 'S', 'M', 'L', 'XL']
    if category_id:
        products_list = Product.objects.filter(category_id=category_id)
    else:
        products_list = Product.objects.all()

    page_number = request.GET.get('page')
    paginator = Paginator(products_list, 6)
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Products Page',
        'categories': ProductCategory.objects.all(),
        'products': page_obj,
        'sizes': sizes,
    }
    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    sizes = ['XS', 'S', 'M', 'L', 'XL']
    context = {
        'title': 'Product Detail',
        'product': product,
        'sizes': sizes,
    }
    return render(request, 'products/product_detail.html', context)