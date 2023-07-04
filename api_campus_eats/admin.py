from django.contrib import admin

from api_campus_eats.models import DishExtra
from api_campus_eats.models import Restaurant
from api_campus_eats.models import Dish
from api_campus_eats.models import CustomerOrder
from api_campus_eats.models import OrderDetail

# Register your models here.
admin.site.register(DishExtra)
admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(CustomerOrder)
admin.site.register(OrderDetail)
