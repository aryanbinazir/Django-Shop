from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from accounts.models import User

class Category(models.Model):
    sub_category = models.ManyToManyField('self',  symmetrical=False, related_name='sbcategory', blank=True)
    is_sub = models.BooleanField(default=False)
    name= models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug])

class Product(models.Model):
     category = models.ManyToManyField(Category, related_name='products')
     name = models.CharField(max_length=200)
     slug = models.SlugField(max_length=100, unique=True)
     image = models.ImageField()
     description = RichTextField(null=True, blank=True)
     available = models.BooleanField(default=True)
     price = models.IntegerField()
     created = models.DateTimeField(auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)

     class Meta:
         ordering = ['name']


     def __str__(self):
         return self.name

     def get_absolute_url(self):
         return reverse('home:product_detail', args=[self.slug])

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pcomments')
    body = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product} - {self.created}'
