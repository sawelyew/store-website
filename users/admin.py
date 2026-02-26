from django.contrib import admin

from users.models import User, Basket

# Register your models here.
admin.site.register(User)
admin.site.register(Basket)