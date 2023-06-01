from rest_framework import viewsets
from api_campus_eats.Serializer import FoodModelSerializer, RestaurantSerializer
from api_campus_eats.models import FoodModel, Restaurant


# Create your views here.
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class FoodModelViewSet(viewsets.ModelViewSet):
    queryset = FoodModel.objects.all()
    serializer_class = FoodModelSerializer
