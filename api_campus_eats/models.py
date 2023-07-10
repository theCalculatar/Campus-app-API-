import datetime
from sqlite3 import Date

from django.contrib.auth.models import User
from django.db import models
import uuid


# Create your models here.
class Restaurant(models.Model):
    restaurant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, unique=True, verbose_name="Name")
    location = models.CharField(max_length=120, verbose_name="Direction")
    phone = models.IntegerField(unique=True)
    isActive = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    restaurant_image = models.ImageField(null=True, upload_to="photos")

    def __str__(self):
        return self.name


class Dish(models.Model):
    dish = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    dish_price = models.DecimalField(max_digits=10, decimal_places=2, )
    name_of_dish = models.CharField(max_length=50, null=False, blank=False)
    type_of_dish = models.CharField(max_length=20, default='Pizza',
                                    choices=[('PIZZA', 'Pizza'), ('MEAL', 'Meal'), ('KOTA', 'Kota'),
                                             ('DINNER', 'Dinner')])
    picture_of_dish = models.ImageField(upload_to='photos', null=False)

    def __str__(self):
        return self.name_of_dish


class DishExtra(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.ManyToManyField(Dish)
    name = models.CharField(max_length=120, unique=True, verbose_name="Name")

    def __str__(self):
        return self.name


class CustomerOrder(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=10, choices=[('COLLECTION', 'collection')
        , ('DELIVER', 'deliver')], default='collection')
    order_status = models.CharField(max_length=20, choices=[
        ("SUBMITTED", "submitted"), ('COMPLETE', 'complete')],
                                    default='submitted')
    # total_amount = models.DecimalField(defau)

    def __str__(self):
        return 'Customer order '+str(self.order_id)[0:4]


class OrderDetail(models.Model):
    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING)
    item_count = models.IntegerField(default=1)
    # dish_extra = models.ForeignKey(DishExtra, on_delete=models.DO_NOTHING, null=True)
