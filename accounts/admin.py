from django.contrib import admin
from .models import CustomUser, Product,Category
from django.contrib.auth.admin import UserAdmin

admin.site.register(Product)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Category)
