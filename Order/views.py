from django.shortcuts import render, redirect
from django.views import View
from .session import OrderSession
from .forms import *
from Home.models import Product
from django.contrib import messages
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from random import randint
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


class OrderListView(View):
    template_name = "Order/order_list.html"
    
    def get(self, request):
        if cart:=request.session.get('cart'):
            basket_objs = OrderSession(request)
            total_price = basket_objs.get_total_price()
            context = {'basket': basket_objs, 'total_price': total_price}
        else:
            context = {'basket': cart}
        return render(request, self.template_name, context)

class AddOrderView(View):

    def post(self, request, product_id):
        form = AddOrderForm(request.POST)
        product = Product.objects.get(pk=product_id)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if not 1 <= quantity <= product.quantity:
                messages.add_message(request, messages.WARNING, f'quantity error!')
            else:
                order = OrderSession(request)
                order.add(product, quantity)
                messages.add_message(request, messages.SUCCESS, f'{quantity} {product.title} added to the basket!')
        else:
            messages.add_message(request, messages.SUCCESS, 'error during add product!')
        return redirect("Home:product_detail", product.slug)

class RemoveOrderView(View):

    def get(self, request, product_id):
        order = OrderSession(request)
        try:
            product = order.remove_order(product_id)
            messages.add_message(request, messages.SUCCESS, f'{product.get("quantity")} {product.get("title")} removed from the basket!')
        except KeyError:
            messages.add_message(request, messages.SUCCESS, f'product not found!')
        return redirect("Order:order_list")


class CheckOutBasketView(LoginRequiredMixin, View):

    
    def get(self, request):
        orders = OrderSession(request)
        if len(orders) != 0:
            base_order_obj, is_created = BaseOrder.objects.get_or_create(user=request.user, paid=False)
            if not is_created:
                base_order_obj.order_items.all().delete()
            for item in orders:
                OrderItem.objects.create(order=base_order_obj, product=Product.objects.get(pk=item['product']['product_id']), quantity=item['quantity'], price=item['product']['price'])
            request.session['check_out'] = True
            request.session['check_out_order'] = base_order_obj.id
            orders.clear()
        else:
            return redirect("Order:order_list")
        return redirect("Order:order_detail", base_order_obj.id)

class OrderDetailView(View):

    def get(self, request, order_id):
        order = BaseOrder.objects.get(id=order_id)
        return render(request, 'Order/order_detail.html', {'order': order})
    

ORDER_PAY_ID = 'order_pay'

class OrderPayView(LoginRequiredMixin, View):

    def get(self, request, order_id):
        if True:
            order = BaseOrder.objects.get(id=order_id)
            refrence_id = f"{str(randint(1000, 9000))}_{order.created_on}"
            request.session[ORDER_PAY_ID] = (order_id, refrence_id)
            return redirect('Order:verify', refrence_id)
        else:
            messages.add_message(request, messages.ERROR, f'error occurd during sending data to zarin pall!')

        return redirect("Order:check_out")
    
class VerifyView(View):

    def get(self, request, refrence_id):
        if refrence_id == (order_session_info:=request.session.get(ORDER_PAY_ID))[1]:
            order = BaseOrder.objects.get(id=order_session_info[0])
            order.paid = True
            order.save()
            order_session = OrderSession(request)
            order_session.clear_check_out_info()

            # decrease product quantities
            proudct_ids = []
            quantity_decrease = []
            for item in order.order_items.all():
                proudct_ids.append(item.product.id)
                quantity_decrease.append(item.quantity)
            products = Product.objects.filter(pk__in=proudct_ids)
            for index, item in enumerate(products):
                item.quantity -= quantity_decrease[index]
                item.save()

            messages.add_message(request, messages.SUCCESS, f'your order succifully buy!')
        else:
            messages.add_message(request, messages.ERROR, f'error occurd during pay your products in payment gateway')
        return redirect("Home:home")

@login_required
def buy_out(request):
    return render(request, "Order/buy_out.html", {'home_message', "Home :)"})


class ApplyCouponView(View):

    def post(self, request, order_id):
        code = request.POST.get("code")
        try:
            coupon = Coupon.objects.get(code__exact=code)
        except Coupon.DoesNotExist:
            messages.error(request, "Coupon code does not exist.", "warning") 
            return redirect("Order:order_detail", order_id)
            
        if coupon.is_active:
            order = BaseOrder.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()

            coupon.use = True
            coupon.save()

            messages.add_message(request, messages.SUCCESS, f'discount applied')
        else:
            messages.error(request, f"Coupon code already used!" if coupon.use else f"coupon code expired!", "warning") 
        return redirect("Order:order_detail", order_id)