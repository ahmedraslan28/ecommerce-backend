from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend

##############################################################

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

##############################################################

from . import serializers
from .models import (Product, Collection, Review, Cart, CartItem)
from .filters import ProductFilter
from .pagination import DefaultPagination


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price']


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(generics.ListCreateAPIView):
    queryset = Collection.objects.annotate(
        product_count=Count('products')).all()

    serializer_class = serializers.CollectionSerializer


class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        product_count=Count('products')).all()

    serializer_class = serializers.CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductReviewList(generics.ListCreateAPIView):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs['pk']
        get_object_or_404(Product, pk=product_id)
        return Review.objects.filter(product=product_id)

    def get_serializer_context(self):
        return {"product_id": self.kwargs["pk"]}


class ProductReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(pk=self.kwargs['pk'], product=self.kwargs['product_id'])


class CartCreate(generics.CreateAPIView):
    serializer_class = serializers.CartSerializer
    queryset = Cart.objects.all()


class CartRetrieve(generics.RetrieveDestroyAPIView):
    serializer_class = serializers.CartSerializer
    queryset = Cart.objects.prefetch_related('items__product').all()


class CartItemsList(generics.GenericAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.CartItemSerializer
        elif self.request.method == 'POST':
            return serializers.AddCartItemSerializer

    def get_queryset(self):
        if self.queryset is not None:
            return self.queryset
        pk = self.kwargs['pk']
        if Cart.objects.filter(pk=pk).exists():
            self.queryset = CartItem.objects.filter(
                cart_id=pk).select_related('product')
            return self.queryset
        raise Http404()

    def get(self, request, pk):
        obj = self.get_queryset()
        serializer = self.get_serializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        context = {"cart_id": pk}
        serializer = self.get_serializer(
            data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CartItemDetail(generics.GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.CartItemSerializer
        elif self.request.method == 'PATCH':
            return serializers.UpdateCartItemSerializer

    def get(self, request, cart_id, pk):
        obj = get_object_or_404(CartItem, pk=pk, cart_id=cart_id)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, cart_id, pk):
        obj = get_object_or_404(CartItem, pk=pk, cart_id=cart_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj.quantity = request.data.get('quantity')
        obj.save()
        return Response(serializer.data)

    def delete(self, request, cart_id, pk):
        obj = get_object_or_404(CartItem, pk=pk, cart_id=cart_id)
        obj.delete()
        return Response({"message": "cart item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class UserRegister(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = None

    # def post(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)


class CustomerCreate(generics.CreateAPIView):
    pass


class CustomerDetail(generics.RetrieveUpdateAPIView):
    pass
