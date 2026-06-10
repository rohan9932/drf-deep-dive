from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


# api view decorator helps to get Request and send Response
# rather than simple HttpRequest, HttpResponse
# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data) 

# class ProductListAPIView(generics.ListAPIView):
#     # queryset = Product.objects.filter(stock__gt=0)
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer # it has built in list() method
 
# class ProductCreateAPIView(generics.CreateAPIView):
#     model = Product
#     serializer_class = ProductSerializer

#     def create(self, request, *args, **kwargs): # overriding default create() method
#         print(request.data)
#         return super().create(request, *args, **kwargs)

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        # at default we are giving access to all
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST': # but changing permission to admin for post method
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('items', 'items__product').all()
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items', 'items__product').all()
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items', 'items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): #overriding the queryset
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=user)


# @api_view(['GET'])
# def products_info(request):
#     products = Product.objects.all()
#     count = len(products)
#     max_price = products.aggregate(max_price=Max('price'))['max_price']
#     serializer = ProductInfoSerializer({
#         'products': products,
#         'count': count,
#         'max_price': max_price
#     })
#     return Response(serializer.data) 

class ProductsInfoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        count = products.count()
        max_price = products.aggregate(max_price=Max('price'))['max_price']
        serializer = ProductInfoSerializer({
            'products': products,
            'count': count,
            'max_price': max_price
        })
        return Response(serializer.data) 
