from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api_campus_eats import Serializer
from api_campus_eats.models import Restaurant, DishExtra, Dish, CustomerOrder


# from rest_framework.permissions import isAuthenticated

class Restaurants(APIView):

    def get(self, request):
        restaurants = Restaurant.objects.filter(isActive=True)
        serializer = Serializer.RestaurantSerializer(restaurants, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = Serializer.RestaurantSerializer(data=request.data,
                                                     context={
                                                         'request': request
                                                     })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantDetail(APIView):

    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            raise Http404

        serializer = Serializer.RestaurantSerializer(restaurant)
        return Response(serializer.data)

    def delete(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            raise Http404
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DishView(APIView):

    def get(self, request, restaurant_id):
        queryset = Dish.objects.filter(restaurant_id=restaurant_id)
        serializer = Serializer.DishSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, restaurant_id):
        try:
            Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            raise Http404

        serializer = Serializer.DishSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(pk=restaurant_id, extras=request.data.get("extras"))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DishDetailsView(APIView):

    def get(self, request, restaurant_id, dish_id):
        try:
            extras = Dish.objects.get(restaurant_id=restaurant_id, dish=dish_id)
        except DishExtra.DoesNotExist:
            raise Http404
        serializer = Serializer.DishSerializer(extras)
        return Response(serializer.data)

    def delete(self, request, restaurant_id, dish_id):
        try:
            menu = Dish.objects.get(restaurant_id=restaurant_id, dish=dish_id)
        except DishExtra.DoesNotExist:
            raise Http404
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetRestaurantOrders(APIView):

    def get(self, request):
        # request is used to check current loggen in user
        order = CustomerOrder.objects.filter(customer_id=request.user.id)
        serializer = Serializer.CustomerOrderSerializer(order, many=True, context={'request': request})
        return Response(serializer.data)


class CreateRestaurantOrder(APIView):

    def get(self, request, restaurant_id):
        # request is used to check current loggen in user
        try:
            Restaurant.objects.get(restaurant_id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise Http404

        order = CustomerOrder.objects.filter(customer_id=request.user.id,
                                             restaurant_id=restaurant_id
                                             )
        serializer = Serializer.CustomerOrderSerializer(order,
                                                        many=True,
                                                        context={'request': request})
        return Response(serializer.data)

    def post(self, request, restaurant_id):

        try:
            Restaurant.objects.filter(restaurant_id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise Http404

        serializer = Serializer.CustomerOrderSerializer(data=request.data,
                                                        context={'request': request,
                                                                 'restaurant_id': restaurant_id}
                                                        )
        if serializer.is_valid():
            serializer.save(order_items=request.data.get('order_items'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCartOrder(APIView):
    # def delete(self,):

    # def post(self, request, order_id):
    #     try:
    #         order = CustomerOrder.objects.get(order_id=order_id,
    #                                           customer_id=request.user.id)
    #     except CustomerOrder.DoesNotExist:
    #         raise Http404
    #
    #     serializer = Serializer.CustomerOrderSerializer(data=request.data)
    #     return Response(serializer.data)

    def get(self, request, order_id):

        try:
            queryset = CustomerOrder.objects.get(order_id=order_id,
                                                 customer_id=request.user.id)
        except CustomerOrder.DoesNotExist:
            raise Http404
        serializer = Serializer.CustomerOrderSerializer(queryset,
                                                        context={'request': request})
        return Response(serializer.data)
