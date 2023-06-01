from django.db import models


# Create your models here.
class FoodModel(models.Model):
    # restaurant_fk = models.ForeignKey()
    food_name = models.CharField(max_length=50, null=False, blank=False)
    food_price = models.DecimalField(max_digits=10, null=False, blank=False, decimal_places=2)
    food_type = models.CharField(max_length=30, null=False, blank=False)
    food_description = models.CharField(max_length=250, null=True, blank=True)
    food_image = models.ImageField(null=False, upload_to="photos")
    food_ratings = models.DecimalField(max_digits=10, null=False, blank=False,  decimal_places=2)
    # food_extras = models.


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=50, null=False, blank=False)
    restaurant_image = models.ImageField(null=False, upload_to="photos")
    restaurant_ratings = models.DecimalField(max_digits=3, null=True, blank=True, decimal_places=2)
    restaurant_description = models.CharField(max_length=250, null=True, blank=True)
    restaurant_location = models.CharField(max_length=30, null=False, blank=False)
