from django.contrib import admin
from .models import Person, Product, ProductFeatures, Category

# Register your models here.

admin.site.register(Person)
admin.site.register(Product)
admin.site.register(ProductFeatures)
admin.site.register(Category)