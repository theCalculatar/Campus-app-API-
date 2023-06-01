from rest_framework import serializers
from api_campus_eats.models import FoodModel, Restaurant


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('pk', 'restaurant_name', "restaurant_image",
                  'restaurant_location', 'restaurant_description',)


class FoodModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FoodModel
        fields = ('pk', 'food_name', "food_price", 'food_type',
                  'food_description', 'food_ratings', 'food_image')
