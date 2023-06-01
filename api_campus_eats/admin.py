from django.contrib import admin

from api_campus_eats.models import FoodModel
from api_campus_eats.models import Restaurant

# Register your models here.
admin.site.register(FoodModel)
admin.site.register(Restaurant)
