from django.db import models
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length= 200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug=slugify(self.category_name)
        super(Category,self).save(*args, **kwargs)

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length= 200, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

    def save(self, *args, **kwargs):
        self.slug=slugify(self.product_name)
        super(Product,self).save(*args, **kwargs)