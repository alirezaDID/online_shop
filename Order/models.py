from django.db import models
from Account.models import CustomUser 
from Home.models import Product
from django.utils import timezone

# Create your models here.


class BaseOrder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, related_name='orders')
    paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(blank=True, null=True)
    class Meta:
        ordering = ("-paid", "-created_on")

    def __str__(self):
        return f"{self.pk} - {self.user.USERNAME_FIELD}"
    
    def get_total_cost(self):
        total = sum(item.get_cost for item in self.order_items.all())
        return total if not self.discount else total - ((self.discount / 100) * total)


class OrderItem(models.Model):
    order = models.ForeignKey(BaseOrder, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    price = models.IntegerField()

    @property
    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product} {self.get_cost}"


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    from_this = models.DateTimeField()
    to_this = models.DateTimeField()
    discount = models.IntegerField(blank=True, null=True)

    use = models.BooleanField(default=False)
    
    @property
    def is_active(self):
        return (not self.use) and (self.from_this <= timezone.now() <= self.to_this)

