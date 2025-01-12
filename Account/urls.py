from django.urls import path, include
from . import views

app_name = "Account"

register_urls = [
    path("", views.RegisterView.as_view(), name='register'),
    path("verify_code/", views.VerifyCodeView.as_view(), name='verify_code'),
    path("send_code_again/", views.SendCodeAgainView.as_view(), name='send_code_again')
]

urlpatterns = [
    path("login/", views.LoginView.as_view(), name='login'),
    path("logout/", views.LogoutView.as_view(), name='logout'),
    
    # register view
    path("register/", include(register_urls))
]
