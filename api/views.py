from django.contrib.auth.models import AbstractUser
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from django_filters.rest_framework import DjangoFilterBackend
from pip._internal import req
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from api.models import Order, OrderItem, Product, User
from api.serializers import (OrderSerializer, ProductInfoSerializer,
                             ProductSerializer, OrderCreateSerializer, UserSerializer)

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
    queryset = Product.objects.order_by('pk') # ordering for consistent pagination result
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend # gonna filter out any product whose stock = 0
    ]
    search_fields = ['=name', 'description'] # if we need exact match then '=' before the field name
    ordering_fields = ['name', 'price', 'stock']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 1
    pagination_class.page_size_query_param = 'size' # giving client a param to control how much data they wanna see in a page
    pagination_class.max_page_size = 3

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



### --- So we want to use OrderSerializer for get method and OrderCreateSerializer for POST method --- ###

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None # to disable pagination for specific view from global pagination
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    # dynamically change to OrderCreateSerializer if it's a post req
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return OrderCreateSerializer
        return super().get_serializer_class()

    # In all the actions the queryset filter is applied by normal users and admin
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user) # filters data to see only normal user's itself's order
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 


    # it becomes redundant
    ## as user based order is already handled in get_queryset()

    # @action(
    #     detail=False,
    #     methods=['get'],
    #     url_path='user-orders',
    #     permission_classes=[IsAuthenticated], # for multiuser auth handle
    # )
    # def user_orders(self, request):
    #     orders = self.get_queryset().filter(user=request.user)
    #     serializer = OrderSerializer(orders, many=True)
    #     return Response(serializer.data)


# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('items', 'items__product').all()
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items', 'items__product').all()
#     serializer_class = OrderSerializer
#
#
# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items', 'items__product').all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self): #overriding the queryset
#         user = self.request.user
#         qs = super().get_queryset()
#         return qs.filter(user=user)


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



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
