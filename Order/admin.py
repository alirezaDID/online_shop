from django.contrib import admin
from .models import *

class OrderItemLinerAdmin(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ("product", )



@admin.register(BaseOrder)
class BaseOrderAdmin(admin.ModelAdmin):
    list_display = ("user", "paid", "created_on", "last_updated")
    list_filter = ('paid', "created_on", "last_updated")
    inlines = (OrderItemLinerAdmin, )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "use")