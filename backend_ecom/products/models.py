from django.db import models
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length= 200, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length= 200, blank=True)
    category = models.ForeignKey(Category,related_name="products", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    # image = models.ImageField(upload_to='products/')
    sold = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=False)
    date_of_sale = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name
    

class CartManagement(models.Model):
    user = models.ForeignKey('app.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class OrderManagement(models.Model):
    user = models.ForeignKey('app.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    PAYMENT_MODES = (
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
    )
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODES)