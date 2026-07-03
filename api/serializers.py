from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    # for accessing order_details related to this product
    # item_orders = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']
        # fields = ['id', 'name', 'description', 'price', 'stock', 'item_orders']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value
 

# this will be nested into the orderserializer
class OrderItemSerializer(serializers.ModelSerializer):
    # for product
    # product = ProductSerializer(read_only=True)
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2
    )

    # for product get request
    # order_user = serializers.CharField(source='order.user.username')
    # order_id = serializers.UUIDField(source='order.order_id')

    class Meta:
        model = OrderItem 
        fields = ['product_name', 'product_price', 'quantity', 'item_subtotal'] # item_subtotal is a property of OrderItem Model

        # fields = ['order_user', 'order_id']


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ['product', 'quantity']

    items = OrderItemCreateSerializer(many=True)
    order_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'user', 'created_at', 'status', 'items']
        extra_kwargs = {
            'user': {'read_only':True}
        }

    def create(self, validated_data):
        order_item_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item in order_item_data:
            OrderItem.objects.create(order=order, **item)

        return order


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True) # so that viewset doesn't want us to generate id
    # nested serializer -> viewing the items of this order from this 
    # serializer 
    # N.B -> the var name must match the related name in the model -> because we 
    # are accessing through reverse relationship
    # eg. As it is fetching from OrderItem so order filed's related name 
    # must be named 'items'
    # handles OrderItem.objects.filter(order_id=order.id)
    items = OrderItemSerializer(many=True, read_only=True)
    # if we don't use OrderItemSerializer it will just return the 
    # items id list  

    # for details -> https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_id', 'user', 'created_at', 'status', 'items', 'total_price']


    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items) 
    

class ProductInfoSerializer(serializers.Serializer):
    # get all products , count of them, max price of all products
    products = ProductSerializer(many=True, read_only=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
