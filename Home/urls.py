from django.urls import path, include
from . import views

app_name = "Home"


urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("category/<slug:cat_slug>", views.HomeView.as_view(), name='category'),
    path("product/<slug:slug>", views.ProductDetailView.as_view(), name='product_detail')
]
