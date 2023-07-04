from rest_framework import serializers
from api_campus_eats import models
from api_campus_eats.models import Dish, OrderDetail, CustomerOrder, DishExtra, Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    # Serializer for the Restaurant model, in fields we specify the model attributes we want to
    # deserialize and serialize
    # isActive = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Restaurant
        fields = ['restaurant_id', 'name', 'location', 'phone', ]


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
    Extras = serializers.SerializerMethodField('get_extras')
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
        fields = ('dish', 'name_of_dish', "type_of_dish", 'dish_price', 'picture_of_dish', 'Extras')


class OrderSerializer(serializers.ModelSerializer):
    dish = DishSerializer()

    class Meta:
        model = OrderDetail
        fields = ['order_id', 'dish', 'item_count']


class CustomerOrderSerializer(serializers.ModelSerializer):
    # used 'get_order_detail' method to get all orders under specific user
    orders = serializers.SerializerMethodField('get_order_detail')

    def get_order_detail(self, obj):
        try:
            order = models.OrderDetail.objects.filter(order_id=obj.order_id)
            return OrderSerializer(order, many=True, context={'request': self.context['request']}).data
        except obj.DoesNotExist:
            return None

    class Meta:
        model = CustomerOrder
        fields = ('order_id', 'order_type', 'order_status', 'orders')

    def create(self, validated_data):

        restaurant_id = self.context['restaurant_id']
        user = self.context.get('request').user

        order = CustomerOrder()
        order.customer_id = user

        try:
            customer_order = CustomerOrder.objects.filter(customer_id=user.id).last()
            restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)

            if customer_order.order_status != 'submitted':
                order.restaurant_id = restaurant
                order.save()
        except CustomerOrder.doesNotExist:
            order.save()
            validated_data['order_id'] = order
            validated_data['restaurant_id'] = restaurant

        order_item = models.OrderDetail.objects.create(**validated_data)
        return order_item
