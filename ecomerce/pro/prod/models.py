from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    product_name = models.CharField(max_length=255, related_name  = "product_name")
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_description = models.TextField(null=True)
    image = models.ImageField(upload_to="product", null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug =  slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.product_name

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    name = models.CharField(max_length=50)  # Small, Medium, Large
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.product_name} - {self.name}"

class SizeColor(models.Model):
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, related_name='colors')
    name = models.CharField(max_length=50)  # Red, Blue, Green
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_color_image = models.ImageField(upload_to="product_color",null=True)

    def __str__(self):
        return f"{self.product_size} - {self.name}"
    
    def final_price(self):
        return self.product_size.product.base_price + self.product_size.price + self.price