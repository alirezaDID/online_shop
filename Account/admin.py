from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import *
from django.contrib import admin
from django.contrib.auth.models import Group


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    readonly_fields = ("last_login", )

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "last_login", "is_admin"]
    list_filter = ['is_admin', "is_seller"]
    fieldsets = [
        (None, 
         {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name"]}),
        ("Permissions", {"fields": ["is_admin", "is_active", "is_superuser", "is_seller", "last_login", 'groups', 'user_permissions']}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "fields": ("email", "password1", "password2"),
            },
        ),
    ]

    def get_form(self, request, obj =None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['is_superuser'].disabled = True

        return form

    search_fields = ["email"]
    ordering = ["last_login"]
    filter_horizontal = ['groups', 'user_permissions']


# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ['email', 'code', 'created_on']
    ordering = ['created_on']
    list_filter = ['email', 'code']
