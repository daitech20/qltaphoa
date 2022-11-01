from itertools import product
from tabnanny import check
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import Product, WareHouse, GoodsReceipt, Expose, PaymentAccount, Payment, OrderItem, Order, Checkout
import django.contrib.auth.password_validation as validators
from django.core import exceptions
import qrcode
import shutil
import pathlib
import base64
from drf_extra_fields.fields import Base64ImageField

from django.core.files.base import ContentFile


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'user':
                         {
                             'id': self.user.id,
                             'username': self.user.username,
                             'email': self.user.email,
                             'first_name': self.user.first_name,
                             'last_name': self.user.last_name,
                             'is_superuser': self.user.is_superuser
                         }
                     })
        # and everything else you want to send in the response
        return data

class CustomJWTSerializer(MyTokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }
        # This is answering the original question, but do whatever you need here.
        # For example in my case I had to check a different model that stores more user info
        # But in the end, you should obtain the username to continue.
        user_obj = User.objects.filter(email=attrs.get("username")).first() or User.objects.filter(username=attrs.get("username")).first()
        if user_obj:
            credentials['username'] = user_obj.username

        return super().validate(credentials)

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'is_superuser',]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match"})
        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=attrs['password'])
            # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


    def create(self, validated_data):
        if User.objects.filter(username=validated_data["username"]).exists():
            raise serializers.ValidationError({"username": "User name already exists"})
        if User.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()
		
        user.is_superuser = False
        user.save()

        return user

class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    image = Base64ImageField()

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'price', 'user', 'barcode', 'id')
        extra_kwargs = {
            'barcode': {
                'required': False
            }
        }
    
    def create(self, validated_data):

        image = validated_data.pop('image')
        user = validated_data.pop('user')
        name = validated_data.pop('name')
        description = validated_data.pop('description')
        price = validated_data.pop('price')

        product = Product.objects.create(user=user, image=image, name=name, description=description, price=price)
        img = qrcode.make(str(product.id))
        
        #print(bracode)
        img.save('qr' + str(product.id) + '.png')
        
        src = pathlib.Path().resolve()


        shutil.move(str(src) + '\qr' + str(product.id) + '.png', str(src) + '\media\images')
        
        product.barcode = '\images' + '\qr' + str(product.id) + '.png'

        #product.bracode=img

        product.save()

        return product
    
    def update(self, instance, validated_data):
       
        return super().update(instance, validated_data)

class WareHouseSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = WareHouse
        fields = '__all__'

    def create(self, validated_data):
        if WareHouse.objects.filter(user=validated_data["user"], product=validated_data["product"]).exists():
            raise serializers.ValidationError({"product": "product already exists"})
        if validated_data["product"] not in Product.objects.filter(user=validated_data["user"]):
            raise serializers.ValidationError({"product": "product already not exists"})
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if validated_data["product"] not in Product.objects.filter(user=instance.user):
            raise serializers.ValidationError({"product": "product already not exists"})

        return super().update(instance, validated_data)

class GoodsReceiptSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = GoodsReceipt
        fields = '__all__'
    
    def create(self, validated_data):
        if validated_data["product"] not in Product.objects.filter(user=validated_data["user"]):
            raise serializers.ValidationError({"product": "product already not exists"})
        
        if WareHouse.objects.filter(user=validated_data["user"], product=validated_data["product"]).exists():
            warehouse =  WareHouse.objects.get(user=validated_data["user"], product=validated_data["product"])
            warehouse.quantity += validated_data["quantity"]
            warehouse.save()
        else:
            warehouse = WareHouse.objects.create(user=validated_data["user"], product=validated_data["product"], quantity=validated_data["quantity"])

        return super().create(validated_data)

class ExposeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Expose
        fields = '__all__'

    def create(self, validated_data):
        if Expose.objects.filter(user=validated_data["user"], product=validated_data["product"]).exists():
            raise serializers.ValidationError({"product": "product already exists"})
        if validated_data["product"] not in Product.objects.filter(user=validated_data["user"]):
            raise serializers.ValidationError({"product": "product already not exists"})
        warehouse = WareHouse.objects.get(product=validated_data["product"])
        if int(validated_data["quantity"]) > warehouse.quantity:
            raise serializers.ValidationError({"product": "Product quantity is not enough"})
        else:
            warehouse.quantity -= int(validated_data["quantity"])
            warehouse.save()
        return super().create(validated_data)
    
    # xem lai
    def update(self, instance, validated_data):
        if validated_data["product"] not in Product.objects.filter(user=instance.user):
            raise serializers.ValidationError({"product": "product already not exists"})
        warehouse = WareHouse.objects.get(product=validated_data["product"])

        if int(validated_data["quantity"]) > instance.quantity:
            quantity = int(validated_data["quantity"]) - instance.quantity
            if quantity > warehouse.quantity:
                raise serializers.ValidationError({"product": "Product quantity is not enough"})
            else:
                warehouse.quantity -= quantity
                warehouse.save()
        else:
            quantity = instance.quantity - int(validated_data["quantity"])
            warehouse.quantity += quantity
            warehouse.save()

        return super().update(instance, validated_data)

class PaymentAccountSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = PaymentAccount
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Payment
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderItemListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Order
        fields = ('user', 'id', )
    
    def create(self, validated_data):
        payment = Payment.objects.create(user=validated_data["user"])
        checkout = Checkout.objects.create(user=validated_data["user"], payment=payment)
        order = Order.objects.create(user=validated_data["user"], checkout=checkout)

        return order

class OrderUpdateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Order
        fields = ('user', 'items', 'id', )
    
    def update(self, instance, validated_data):
        items = validated_data["items"]
        instance.items.clear()
        for item in items:
            instance.items.add(item)
        instance.save()
        checkout = Checkout.objects.get(id=instance.checkout.id)
        checkout.amount = instance.get_total()
        instance.amount = instance.get_total()
        checkout.save()
        instance.save()
        return instance

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    items = OrderItemListSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'

class CheckoutSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Checkout
        fields = '__all__'
    
class CheckoutUpdateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Checkout
        fields = ('user', 'payment_type', 'status')

    def update(self, instance, validated_data):
        instance.payment_type = validated_data["payment_type"]
        instance.status = validated_data["status"]
        order = Order.objects.get(checkout=instance)
        order.status = 0
        order.save()
        instance.save()
        return instance