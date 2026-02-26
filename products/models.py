from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    SIZE_TYPES = [
        (None, 'Без размера (Канцелярия)'),
        ('clothing', 'Одежда (XS, S, M, L, XL)'),
        ('shoes', 'Обувь (36-45)'),
    ]
    size_type = models.CharField(choices=SIZE_TYPES, max_length=20, blank=True, null=True)


    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='products_images', null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return f"{self.name}, {self.price}, {self.description}"