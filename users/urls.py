app_name = 'users'

from django.urls import path
from .views import (profile, login, register, logout, basket_add,
                    basket_remove, basket_edit, create_order, order_view, order_history)

urlpatterns = [
    path('profile', profile, name='profile'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('register', register, name='register'),
    path('basket/add/<int:product_id>', basket_add, name='basket_add'),
    path('basket/remove/<int:product_id>', basket_remove, name='basket_remove'),
    path('basket/edit/<int:product_id>', basket_edit, name='basket_edit'),
    path('create_order', create_order, name='create_order'),
    path('order', order_view, name='order_view'),
    path('order_history', order_history, name='order_history'),
]