from ast import Delete
from django.shortcuts import render
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CheckoutSerializer, CheckoutUpdateSerializer, CustomJWTSerializer, OrderCreateSerializer, OrderItemListSerializer, OrderSerializer, OrderUpdateSerializer, PaymentSerializer, ProductSerializer, RegisterSerializer, WareHouseSerializer, GoodsReceiptSerializer, ExposeSerializer, PaymentAccountSerializer, OrderItemSerializer
from .models import Expose, Product, WareHouse, GoodsReceipt, PaymentAccount, Payment, Order, OrderItem, Checkout
from rest_framework import generics, status
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ProductCreate(generics.CreateAPIView):
    queryset = Product
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Product.objects.all()
        return Product.objects.filter(user=user)

class ProductUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'

class WareHouseCreate(generics.CreateAPIView):
    queryset = WareHouse
    serializer_class = WareHouseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WareHouseList(generics.ListAPIView):
    queryset = WareHouse.objects.all()
    serializer_class = WareHouseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return WareHouse.objects.all()
        return WareHouse.objects.filter(user=user)

class WareHouseUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = WareHouse
    serializer_class = WareHouseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'

class GoodsReceiptCreate(generics.CreateAPIView):
    queryset = GoodsReceipt
    serializer_class = GoodsReceiptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoodsReceiptList(generics.ListAPIView):
    queryset = GoodsReceipt.objects.all()
    serializer_class = GoodsReceiptSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return GoodsReceipt.objects.all()
        return GoodsReceipt.objects.filter(user=user)

class ExposeCreate(generics.CreateAPIView):
    queryset = Expose
    serializer_class = ExposeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExposeList(generics.ListAPIView):
    queryset = Expose.objects.all()
    serializer_class = ExposeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Expose.objects.all()
        return Expose.objects.filter(user=user)

class ExposesUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expose
    serializer_class = ExposeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'

class PaymentAccountCreate(generics.CreateAPIView):
    queryset = PaymentAccount
    serializer_class = PaymentAccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentAccountList(generics.ListAPIView):
    queryset = PaymentAccount.objects.all()
    serializer_class = PaymentAccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PaymentAccount.objects.all()
        return PaymentAccount.objects.filter(user=user)

class PaymentAccountUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentAccount
    serializer_class = PaymentAccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'

class PaymentCreate(generics.CreateAPIView):
    queryset = Payment
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Payment.objects.all()
        return Payment.objects.filter(user=user)

class PaymentUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'

class OrderItemCreate(generics.CreateAPIView):
    queryset = OrderItem
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderItemList(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemListSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(user=user)

class OrderItemDetail(generics.RetrieveAPIView):
    queryset = OrderItem
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

class OrderItemUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'

class OrderCreate(generics.CreateAPIView):
    queryset = Order
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=user)

class OrderDetail(generics.RetrieveAPIView):
    queryset = Order
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

class OrderUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order
    serializer_class = OrderUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['id'])
        checkout = Checkout.objects.get(id=order.id)
        checkout.status = 1
        checkout.save()
        for item in order.items.all():
            item.delete()

        return super(OrderUpdate, self).destroy(request, *args, **kwargs)

class CheckoutList(generics.ListAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Checkout.objects.all()
        return Checkout.objects.filter(user=user)

class CheckoutDetail(generics.RetrieveAPIView):
    queryset = Checkout
    serializer_class = CheckoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

class CheckoutUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checkout
    serializer_class = CheckoutUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'