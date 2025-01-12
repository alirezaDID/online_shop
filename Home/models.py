from django.db import models
from django.urls import reverse
from django.utils.text import slugify 
from Account.models import CustomUser
from uuid import uuid4
# Create your models here.

class ProductCustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)
    


class Category(models.Model):
    # relation fields
    reply_cat = models.ForeignKey('self' ,related_name="childs", on_delete=models.RESTRICT, null=True, blank=True)

    # primery keys
    slug = models.SlugField(max_length=255, unique=True, default=uuid4())

    # ordinary fields
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    cat_img = models.ImageField(upload_to='images/', blank=True, null=True)

    # configurations
    class Meta:
        ordering = ("-created_on", )
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return f"{self.name}"
    
    def save(self):
        if self.name:
            self.slug = slugify(self.name)
        return super().save()
    
    def get_absolute_url(self):
        return reverse("Home:category", args=[self.slug])
    


class Product(models.Model):
    # realtion fileds
    user = models.ForeignKey(CustomUser, related_name='products', on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name="products")

    # primary keys
    slug = models.SlugField(max_length=255, unique=True, default=uuid4())

    # ordinary feilds
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_available = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    price = models.IntegerField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    # managers
    available_products = ProductCustomManager()
    objects = models.Manager()

    # configurations
    class Meta:
        ordering = ('-created_on', 'user')

    def __str__(self):
        return f"{self.title}"
    
    def save(self):
        if self.title:
            self.slug = slugify(self.title)
        return super().save()
    
    def get_absolute_url(self):
        return reverse("Home:product_detail", args=[self.slug])
    




