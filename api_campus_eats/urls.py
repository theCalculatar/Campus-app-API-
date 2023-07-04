from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers

from api_campus_eats import views

from api_campus_eats.models import Restaurant

router = routers.DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('get-restaurants/', views.Restaurants.as_view(), name="Restaurants"),
    path(r'get-restaurant/<str:restaurant_id>/', views.RestaurantDetail.as_view()),
    path(r'restaurants/<str:restaurant_id>/menu/', views.DishView.as_view()),
    path(r'restaurants/<str:restaurant_id>/menu/<str:dish_id>/', views.DishDetailsView.as_view()),
    path(r'create-order/<str:restaurant_id>/', views.CreateRestaurantOrder.as_view()),
    path(r'get-orders/', views.GetRestaurantOrders.as_view()),
    # path('users')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
