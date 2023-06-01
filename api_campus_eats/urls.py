from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers

from api_campus_eats.models import FoodModel, Restaurant
from api_campus_eats.views import FoodModelViewSet, RestaurantViewSet

router = routers.DefaultRouter()
router.register(r'Restaurants', RestaurantViewSet, basename=Restaurant)
router.register(r'FoodModel', FoodModelViewSet, basename=FoodModel)

urlpatterns = [
    path('', include(router.urls))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
