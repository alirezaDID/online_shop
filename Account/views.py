from django.shortcuts import render, HttpResponse, redirect
from django.views import View

from .forms import *
from .models import *

from utilites import send_code
from django.contrib import messages
from random import randint

from datetime import timedelta, datetime
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from Account.mixins import NoLoginRequireMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(NoLoginRequireMixin, View):
    form_class = RegisterForm
    template_name = 'Account/register.html'
    def get(self, requset):
        form = self.form_class
        return render(requset, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = randint(1, 9999)
            send_code(cd['email'], random_code)
            request.session['user_register_info'] = {
                'email': cd['email'],
                'password': cd['password2']
            }
            otp_obj = OtpCode.objects.filter(email=cd['email'])
            if not otp_obj.exists(): 
                OtpCode.objects.create(email=cd['email'], code=random_code)
                messages.add_message(request, messages.SUCCESS, 'verify code sent!')           
            else:
                messages.add_message(request, messages.SUCCESS, 'verify code already sent to you, you can use it or click send code again!') 

            return redirect("Account:verify_code")

        return render(request, self.template_name, {'form':form})


class LoginView(NoLoginRequireMixin, View):
    form_class = LoginForm
    template_name = 'Account/login.html'

    def get(self, requeset):
        form = self.form_class
        return render(requeset, self.template_name,{'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password']) 
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'you succifully logedin!')
                return redirect("Home:home")
            else:
                messages.add_message(request, messages.SUCCESS, f"username or password isn't currect!")
        return render(request, self.template_name, {'form': form})
    

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'logout succifully')
        return redirect("Home:home")


# verify and send again code 
class VerifyCodeView(NoLoginRequireMixin, View):
    form_class = OtpCodeForm
    template_name = 'Account/verify.html'

    def get(self, requeset):
        form = self.form_class
        return render(requeset, self.template_name,{'form': form})

    def post(self, request, ):
        form = self.form_class(request.POST)
        user_register_info = request.session["user_register_info"]
        otp_obj = OtpCode.objects.get(email=user_register_info['email'])
        if form.is_valid():
            cd = form.cleaned_data
            if otp_obj.code == cd['code']:
                CustomUser.objects.create(
                    email = user_register_info['email'],
                    password = user_register_info['password'],         
                )
                otp_obj.delete()
                messages.add_message(request, messages.SUCCESS, "you succifully registerd! now login with your register info")
                return redirect("Account:login")
            else:
                messages.add_message(request, messages.SUCCESS, "verify code is wrong!")
        return render(request, self.template_name, {'form':form})


class SendCodeAgainView(NoLoginRequireMixin ,View):
    form_class = OtpCodeForm

    def post(self, request):
        email = request.session['user_register_info']['email']
        otp_obj = OtpCode.objects.get(email=email)


        if not otp_obj.is_expire():
            messages.add_message(request, messages.SUCCESS, f"wait for {otp_obj.expire_time.seconds} seconds to send code again! ")
        else:
            another_random_code = randint(1, 9999)
            send_code(email, another_random_code)
            otp_obj.code_time = timezone.now() + timedelta(minutes=2)
            otp_obj.code = another_random_code
            otp_obj.save()
            messages.add_message(request, messages.SUCCESS, f"code sent to you again! ")

        return redirect("Account:verify_code")
        