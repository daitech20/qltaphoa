from distutils.command.upload import upload
from email.mime import image
from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATUS = (
    (0, 'success'),
    (1, 'fail'),
    (2, 'processing')
)

PaymentType = (
    (0, 'Tien mat'),
    (1, 'Momo')
)

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_users')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    barcode = models.ImageField(upload_to='images/', blank=True, null=True)
    price = models.FloatField()

class WareHouse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='warehouse_users')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='warehouse_products')
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('user', 'product')

class GoodsReceipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goodsreceipt_users')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='goodsreceipt_products')
    quantity = models.IntegerField()
    amount = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

class Expose(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expose_users')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='expose_products')
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('user', 'product')

class PaymentAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='paymentaccount_users', unique=True)
    account = models.CharField(max_length=20)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_users')
    amount = models.FloatField(null=True, blank=True)
    partnerName = models.CharField(max_length=30, null=True, blank=True)
    partnerId = models.CharField(max_length=11, null=True, blank=True)
    phoneUser = models.CharField(max_length=11, null=True, blank=True)
    comment = models.CharField(max_length=30, null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=2)
    created = models.DateTimeField(auto_now_add=True)

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkout_users')
    status = models.IntegerField(choices=STATUS, default=2)
    amount = models.FloatField(null=True, blank=True)
    payment_type = models.IntegerField(choices=PaymentType, default=0)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='checkout_payments', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orderitem_users')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderitem_products')
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_users')
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name='order_checkouts')
    items = models.ManyToManyField(OrderItem, blank=True)
    amount = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=2)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        self.amount = total
        return total