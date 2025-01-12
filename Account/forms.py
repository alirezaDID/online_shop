from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate
from utilites import *


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password1', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("email", 'password')

    def clean(self):
        cd = self.cleaned_data
        password_validation = PasswordValidation(cd['password1'], cd['password2'])
        password_validation.same_password_validation()
        # password_validation.strong_validation()
        return cd
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user
        
class CustomUserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(help_text='you can change the password from this form : <a href="../password/">this form</a>')

    class Meta:
        model = CustomUser
        fields = ('password', 'email', 'first_name', 'last_name')


class RegisterForm(CustomUserCreationForm):
        class Meta:
            model = CustomUser
            fields = ("email", "password1")


class OtpCodeForm(forms.Form):
    code = forms.IntegerField(max_value=9999)


class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password")
    
    def clean(self):
        cd = self.cleaned_data
        email = str(cd['email']).strip()
        password = str(cd['password']).strip()
        if not email or not password:
            raise ValidationError("password or username are required!")
        return cd
