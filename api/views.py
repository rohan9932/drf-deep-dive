from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view


# api view decorator helps to get Request and send Response
# rather than simple HttpRequest, HttpResponse
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data) 


@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def order_list(request):
    orders = Order.objects.prefetch_related('items', 'items__product').all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def products_info(request):
    products = Product.objects.all()
    count = len(products)
    max_price = products.aggregate(max_price=Max('price'))['max_price']
    serializer = ProductInfoSerializer({
        'products': products,
        'count': count,
        'max_price': max_price
    })
    return Response(serializer.data) 