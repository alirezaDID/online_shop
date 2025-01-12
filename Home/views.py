from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views import View
from django.views.generic import ListView, View
from .models import *

class HomeView(ListView):
    paginate_by = 2
    template_name = 'home/home.html'
    context_object_name = 'list_objs'

    def get_queryset(self):
        list_objs = Product.available_products.all()
        cat_slug=self.kwargs.get("cat_slug")
        if cat_slug:=(self.kwargs.get('cat_slug')):
            category = get_object_or_404(Category, slug=cat_slug)   
            if not category.reply_cat:
                list_objs = category.childs.all()
            else:
                list_objs = list_objs.filter(category=category)
        return list_objs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(reply_cat=None)
        return context

    
class ProductDetailView(View):

    def get(self, request, slug):
        product = get_object_or_404(Product.available_products.all(), slug=slug)
        session_quanity_value = None
        try:
            session_quanity_value = request.session['cart'][str(product.id)]['quantity']
        except:
            session_quanity_value = 1
        context = {
            'product': product,
            'session_quanity_value':  session_quanity_value
        }
        return render(request, 'home/product.html', context)

    