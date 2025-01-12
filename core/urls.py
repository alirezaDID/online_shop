from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("Account.urls", namespace='Account')),
    path("", include("Home.urls", namespace='Home' )),
    path("order/", include("Order.urls", namespace='Order' )),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
