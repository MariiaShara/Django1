from django.contrib import admin

# Register your models here.
from mainapp.models import Clothing, ClothingCategory

admin.site.register(ClothingCategory)
admin.site.register(Clothing)
