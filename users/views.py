from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from users.models import Basket, Product, OrderItem, Order
import requests
from django.conf import settings
import os
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('users:profile')
        else:
            print(form.errors)
            messages.warning(request, 'Profile update failed')
    else:
        form = UserProfileForm(instance=request.user)

    baskets = Basket.objects.filter(user=request.user)

    context = {
        'title': 'Profile',
        'form': form,
        'baskets': baskets,
    }
    return render(request, 'profile.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful')
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Register',
        'form': form,
    }
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(request, email=email, password=password)

            if user:
                auth.login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Неверный логин или пароль.')
    else:
        form = UserLoginForm()

    context = {
        'title': 'Авторизация',
        'form': form,
    }
    return render(request, 'login.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect('index')


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.category.size_type == 'clothing':
        size = request.GET.get('size')
        basket, created = Basket.objects.get_or_create(user=request.user, product_id=product_id, size=size)
    else:
        basket, created = Basket.objects.get_or_create(user=request.user, product_id=product_id)
    if not created:
        basket.quantity += 1
    else:
        basket.quantity = 1
    basket.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.category.size_type == 'clothing':
        size = request.GET.get('size')
        basket = Basket.objects.get(user=request.user, product_id=product_id, size=size)
    else:
        basket = Basket.objects.get(user=request.user, product_id=product_id)
    basket.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_edit(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        if product.category.size_type == 'clothing':
            size = request.GET.get('size')
            basket = Basket.objects.get(user=request.user, product_id=product.id, size=size)
        else:
            basket = Basket.objects.get(user=request.user, product_id=product.id)
        new_quantity = int(request.POST['quantity'])
        if new_quantity > 0:
            basket.quantity = new_quantity
            basket.save()
        else:
            basket.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def order_view(request):
    baskets = Basket.objects.filter(user=request.user)
    if not baskets.exists():
        return redirect('products:index')

    context = {
        'title': 'Оформление заказа',
        'baskets': baskets,
    }
    return render(request, 'order.html', context)


def send_telegram_message(order):

    text = f"🛍 **Новый заказ №{order.id}**\n"
    text += f"👤 Покупатель: @{order.telegram_contact}\n"
    text += f"📧 Email: {order.user.email}\n\n"
    text += "📦 **Товары:**\n"

    for item in order.items.all():
        text += f"- {item.product.name} ({item.size}) — {item.quantity} шт.\n"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Ошибка отправки в ТГ: {e}")


@login_required
def create_order(request):
    if request.method == 'POST':
        tg_contact = request.POST.get('telegram_contact')
        baskets = Basket.objects.filter(user=request.user)
        if not baskets.exists():
            return redirect('index')

        order = Order.objects.create(user=request.user, telegram_contact=tg_contact)
        for basket in baskets:
            OrderItem.objects.create(order=order, product=basket.product, quantity=basket.quantity, size=basket.size)

        send_telegram_message(order)
        baskets.delete()
        messages.success(request, 'Заказ успешно завершен.')
        return redirect('products:index')
    else:
        return redirect('users:profile')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'title': 'История заказов',
        'orders': orders,
    }
    return render(request, 'order_history.html', context)

