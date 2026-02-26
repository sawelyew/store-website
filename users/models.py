from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import Product

def get_dictionary_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = f'avatar.{extension}'
    return f'users/user_{instance.id}/{filename}'

class User(AbstractUser):
    image = models.ImageField(upload_to=get_dictionary_path, null=True, blank=True)


class BasketQuerySet(models.QuerySet):
    def total_price(self):
        price = sum(basket.sum() for basket in self)
        return price

    def total_quantity(self):
        total = sum(basket.quantity for basket in self)
        return total

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    objects = BasketQuerySet.as_manager()
    size = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Корзина для {self.user.username} | Товар: {self.product.name} | Размер: {self.size} | Количество: {self.quantity}"

    class Meta:
        unique_together = ('user', 'product', 'size')
        verbose_name = "Корзина товаров"
        verbose_name_plural = "Корзины товаров"

    def sum(self):
        return self.quantity*self.product.price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    telegram_contact = models.CharField(max_length=30)
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Заказ №{self.id} ({self.user.email})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, null=True, blank=True)