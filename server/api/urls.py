from django.urls import path
import include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import CheckoutDetail, MyTokenObtainPairView, OrderDetail, OrderItemCreate, OrderItemDetail, OrderItemList, OrderItemUpdate, OrderList, OrderUpdate, PaymentCreate, PaymentList, PaymentUpdate, RegisterView, \
    ProductCreate, ProductList, ProductUpdate, WareHouseCreate, \
    WareHouseList, WareHouseUpdate, GoodsReceiptCreate, GoodsReceiptList, ExposeCreate, \
    ExposeList, ExposesUpdate, PaymentAccountCreate, PaymentAccountList, PaymentAccountUpdate, \
    OrderCreate, CheckoutList, CheckoutUpdate

urlpatterns = [
    path('api/product/create', ProductCreate.as_view(), name='products_create'),
    path('api/products', ProductList.as_view(), name='products_list'),
    path('api/product/update/<int:id>', ProductUpdate.as_view(), name='products_update'),
    path('api/warehouse/create', WareHouseCreate.as_view(), name='warehouses_create'),
    path('api/warehouses', WareHouseList.as_view(), name='warehouses_list'),
    path('api/warehouse/update/<int:id>', WareHouseUpdate.as_view(), name='warehouses_update'),
    path('api/goodsreceipt/create', GoodsReceiptCreate.as_view(), name='goodsreceipts_create'),
    path('api/goodsreceipts', GoodsReceiptList.as_view(), name='goodsreceipts_list'),
    path('api/expose/create', ExposeCreate.as_view(), name='exposes_create'),
    path('api/exposes', ExposeList.as_view(), name='exposes_list'),
    path('api/expose/update/<int:id>', ExposesUpdate.as_view(), name='exposes_update'),
    path('api/paymentaccount/create', PaymentAccountCreate.as_view(), name='paymentaccounts_create'),
    path('api/paymentaccounts', PaymentAccountList.as_view(), name='paymentaccounts_list'),
    path('api/paymentaccount/update/<int:id>', PaymentAccountUpdate.as_view(), name='paymentacounts_update'),
    path('api/payment/create', PaymentCreate.as_view(), name='payments_create'),
    path('api/payments', PaymentList.as_view(), name='payments_list'),
    path('api/payment/update/<int:id>', PaymentUpdate.as_view(), name='payments_update'),
    path('api/orderitem/create', OrderItemCreate.as_view(), name='orderitems_create'),
    path('api/orderitems', OrderItemList.as_view(), name='orderitems_list'),
    path('api/orderitem/<int:id>', OrderItemDetail.as_view(), name='orderitems_detail'),
    path('api/orderitem/update/<int:id>', OrderItemUpdate.as_view(), name='orderitems_update'),
    path('api/order/create', OrderCreate.as_view(), name='orders_create'),
    path('api/orders', OrderList.as_view(), name='orders_list'),
    path('api/order/<int:id>', OrderDetail.as_view(), name='orders_detail'),
    path('api/order/update/<int:id>', OrderUpdate.as_view(), name='orders_update'),
    path('api/checkouts', CheckoutList.as_view(), name='checkouts_list'),
    path('api/checkout/update/<int:id>', CheckoutUpdate.as_view(), name='checkouts_update'),
    path('api/checkout/<int:id>', CheckoutDetail.as_view(), name='checkouts_detail'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register', RegisterView.as_view()),
]
