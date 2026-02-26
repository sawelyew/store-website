app_name = 'products'

from django.urls import path
from products.views import products, product_detail

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:category_id>/', products, name='category'),
    path('<int:product_id>/', product_detail, name='product_detail'),
]