from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", 'reply_cat')