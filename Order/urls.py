from django.urls import path, include
from . import views

app_name = "Order"

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('add_order/<int:product_id>', views.AddOrderView.as_view(), name='add_order'),
    path('remove_order/<int:product_id>', views.RemoveOrderView.as_view(), name='remove_order'),
    path('check_out/', views.CheckOutBasketView.as_view(), name='check_out'),
    path('order_detail/<int:order_id>', views.OrderDetailView.as_view(), name='order_detail'),

    path('order_pay/<int:order_id>', views.OrderPayView.as_view(), name='order_pay'),
    path('verify/<str:refrence_id>', views.VerifyView.as_view(), name='verify'),
    path('buy_out/', views.buy_out, name='buy_out'),
    
    path('apply_coupon/<int:order_id>', views.ApplyCouponView.as_view(), name='apply_coupon'),
]