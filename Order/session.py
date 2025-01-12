from Home.models import *
from django.contrib import messages
from copy import deepcopy

CART_SESSION_ID = 'cart'

class OrderSession:
    def __init__(self, request):
        self.total_price = 0
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            self.session[CART_SESSION_ID] = {}
            cart = self.session[CART_SESSION_ID]
        self.cart = cart

    def add(self, product: Product, quantity):
        product_id = product.id
        if not self.cart.get(str(product_id)):
            self.cart[product_id] = {
                'product': {
                    'title': product.title,
                    'price': product.price,
                    'product_id': product.id
                },
                'quantity': quantity, 
                'total_price': product.price * quantity
            }
        else:
            if self.cart[product_id]['quantity'] != quantity:
                self.cart[product_id]['quantity'] = quantity

        self.save()


    def save(self):
            self.session.modified = True


    def remove_order(self, product_id):
        product = deepcopy(self.cart[str(product_id)])
        del self.cart[str(product_id)]
        self.save()
        return product


    def get_total_price(self):
        return sum(int(item['total_price']) for item in self.cart.values())


    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def clear_check_out_info(self):
        del self.session['check_out']
        del self.session['check_out_order']
        self.save()

    # magic functions
    def __iter__(self):
        cart = self.cart.copy()
        product_keys = cart.keys()
        products = Product.objects.filter(pk__in=product_keys)
        for index, item in enumerate(cart.values()):
            item['product'] = {
                    'title': products[index].title,
                    'price': products[index].price,
                    'product_id': products[index].id
                    }
            item['total_price'] = str(int(item['product']['price']) * int(item['quantity']))
            yield item


    def __len__(self):
        return len(self.cart.keys())