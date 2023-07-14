from django.http import Http404
from rest_framework import serializers, status
from api_campus_eats import models
from api_campus_eats.models import Dish, OrderDetail, CustomerOrder, DishExtra, Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    # Serializer for the Restaurant model, in fields we specify the model attributes we want to
    # deserialize and serialize

    class Meta:
        model = models.Restaurant
        fields = ('restaurant_id', 'name', 'location', 'phone')

    def create(self, validated_data):
        owner = self.context.get('request').user.id
        validated_data["owner_id"] = owner
        return models.Restaurant.objects.create(**validated_data)


class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DishExtra
        fields = ['id', 'name']


class DishSerializer(serializers.ModelSerializer):
    # As each Extra has an image thumbnail we deal with the serialization of the image in the function
    # 'encode_thumbnail' were the image is read from the media folder and encoded into base64
    # thumbnail = serializers.SerializerMethodField('encode_thumbnail')
    # When getting an Extras I want an 'Extras' field, the value of this field is the return of the get_Extras
    # function that serializes the Extras for the Extras.
    # Extras = serializers.SerializerMethodField('get_extras')
    picture_of_dish = serializers.SerializerMethodField('get_image_url')

    # def encode_thumbnail(self, Extras):
    #     with open(os.path.join(settings.MEDIA_ROOT, Extras.thumbnail.name), "rb") as image_file:
    #         return base64.b64encode(image_file.read())

    # use method to return url instead of directory

    def get_image_url(self, obj):
        request = self.context['request']
        image_url = obj.picture_of_dish.url
        return request.build_absolute_uri(image_url)

    def get_extras(self, obj):
        try:
            extras_extras = DishExtra.objects.filter(menu=obj.dish)
            return ExtraSerializer(extras_extras, many=True).data
        except DishExtra.DoesNotExist:
            return None

    def create(self, validated_data):
        """
        Create function for Dish, a restaurant and a list of Extras is associated. The restaurantId
        is taken from the corresponding path parameter and the Extras can be added optionally in the post body.
        """
        extras_data = validated_data.pop("extras")
        restaurant = models.Restaurant.objects.get(pk=validated_data["restaurant_id"])
        validated_data["restaurant"] = restaurant
        menu = models.Dish.objects.create(**validated_data)

        # Assign Extras if they are present in the body
        if extras_data:
            for extra_dict in extras_data:
                extra = models.DishExtra(name=extra_dict["name"])
                extra.save()
                extra.menu.add(menu)
        return menu

    class Meta:
        model = Dish
        fields = ('dish', 'name_of_dish', 'type_of_dish',
                  'dish_price', 'picture_of_dish')


class OrderSerializer(serializers.ModelSerializer):
    dish = DishSerializer()

    class Meta:
        model = OrderDetail
        fields = ['order_id', 'item_count', 'dish']


class CustomerOrderSerializer(serializers.ModelSerializer):
    # used 'get_order_detail' method to get all orders under specific user
    order_items = serializers.SerializerMethodField('get_order_detail')

    def get_order_detail(self, obj):
        try:
            order = models.OrderDetail.objects.filter(order_id=obj.order_id)
            return OrderSerializer(order, many=True, context={'request': self.context['request']}).data
        except obj.DoesNotExist:
            return None

    class Meta:
        model = CustomerOrder
        fields = ('order_id', 'customer_id', 'order_type', 'restaurant_id',
                  'order_status', 'order_items',)

    def create(self, validated_data):

        restaurant_id = self.context['restaurant_id']
        user = self.context.get('request').user

        items = validated_data.pop('order_items')

        try:
            restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
            validated_data['restaurant_id'] = restaurant  # assign restaurant instance
            validated_data['customer_id'] = user
            # get last order object
            order = CustomerOrder.objects.get(customer_id=user.id, order_status="submitted")

        except CustomerOrder.DoesNotExist:
            order = models.CustomerOrder.objects.create(**validated_data)

        if items:
            for each_item in items:
                dish = Dish.objects.get(pk=each_item['dish']['dish'])
                try:
                    OrderDetail.objects.get(order=order)
                    OrderDetail.objects.filter(order=order).update(item_count=1
                    if each_item['item_count'] <= 0 else each_item['item_count'])
                except OrderDetail.DoesNotExist:
                    OrderDetail.objects.create(order=order, dish=dish, item_count=1
                    if each_item['item_count'] <= 0 else each_item['item_count'])

        return order


class CartOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrder
        fields = ('order_id', 'customer_id', 'order_type', 'restaurant_id',
                  'order_status', 'order_items',)
