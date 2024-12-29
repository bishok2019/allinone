from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
# Create your models here.

class Category(BaseModel):
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to="categories")

    def save(self, *args, **kwargs):
        self.slug =  slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name
    
class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product")
    base_price = models.IntegerField()
    product_description = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug =  slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.product_name

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images", null=True)
    image = models.ImageField(upload_to="product")

    def __str__(self):
        return f"Image for {self.product.product_name}"

class SizeVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    size_name = models.CharField(max_length=100)
    additional_price = models.IntegerField(default=0)

    def __str__(self):
        return self.size_name
    
class ColorVariant(BaseModel):
    size = models.ForeignKey(SizeVariant, on_delete=models.CASCADE,null = True)
    color_name = models.CharField(max_length=100)
    additional_price = models.IntegerField(default=0)

    def __str__(self):
        return self.color_name

class ProductColorImage(BaseModel):
    color = models.ForeignKey(ColorVariant, on_delete=models.CASCADE)
    product_color_image = models.ImageField(upload_to="product_color",null=True)

    # def __str__(self):
    #     return self.product_color_image
