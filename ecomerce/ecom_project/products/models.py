from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from accounts.models import Profile
from django.db.models import F, Sum
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
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

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product")
    product_name = models.CharField(max_length=255)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_description = models.TextField(null=True)
    image = models.ImageField(upload_to="product", null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug =  slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.product_name

class SizeVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_sizes", null=True)
    size_name = models.CharField(max_length=100)
    additional_price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.size_name}-{self.product.product_name}"
    
class ColorVariant(BaseModel):
    size = models.ForeignKey(SizeVariant, on_delete=models.CASCADE,related_name="product_colors",null = True)
    color_name = models.CharField(max_length=100, null=True)
    additional_price = models.IntegerField(default=0)
    product_color_image = models.ImageField(upload_to="product_color",null=True)
    total_quantity = models.IntegerField(null = True)

    def __str__(self):
        return f"{self.color_name}-{self.size.size_name}-{self.size.product.product_name}"
    
    def final_price(self):
        return self.additional_price + self.size.additional_price + self.size.product.base_price

# class Cart(models.Model):
#     cart_owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="carts")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_paid = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Cart for {self.cart_owner.user.username}"
    
#     def get_cart_total(self):
#         return sum(item.get_item_price() for item in self.cart_items.all())
    
#     def get_total_items(self):
#         return sum(item.quantity for item in self.cart_items.all())
    
#     def add_to_cart(self, color_variant, quantity):
#         current_quantity = self.cart_items.filter(color_variant=color_variant).aggregate(total=Sum('quantity'))['total'] or 0
#         # print(current_quantity)
#         available_stock = color_variant.total_quantity - current_quantity
#         if quantity>available_stock:
#             raise ValidationError(
#                 f"Cannot add {quantity} items. Only {available_stock} available for {color_variant}"
#             )
#         cart_item, created = self.cart_items.get_or_create(color_variant=color_variant)
#         cart_item.quantity += quantity
#         cart_item.save()
#     def place_order(self):
#         """Finalize the order, ensuring no over-ordering of stock."""
#         for cart_item in self.carts.cart_items.all():
#             color_variant = cart_item.color_variant
#             quantity = cart_item.quantity

#             # Validate stock
#             current_stock = color_variant.total_quantity
#             if quantity > current_stock:
#                 raise ValidationError(
#                     f"Cannot place order for {quantity} items of {color_variant}. Only {current_stock} available."
#                 )
            
#             # Deduct stock
#             color_variant.total_quantity -= quantity
#             color_variant.save()
        
#         # Mark cart as paid
#         self.cart.is_paid = True
#         self.cart.save()
class Cart(BaseModel):
    cart_owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart for {self.cart_owner.user.username}"
    
    def get_cart_total(self):
        return sum(item.get_item_price() for item in self.cart_items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.cart_items.all())
    
    def add_to_cart(self, color_variant, quantity):
        current_quantity = self.cart_items.filter(color_variant=color_variant).aggregate(total=Sum('quantity'))['total'] or 0
        available_stock = color_variant.total_quantity - current_quantity
        if quantity > available_stock:
            raise ValidationError(
                f"Cannot add {quantity} items. Only {available_stock} available for {color_variant}"
            )
        cart_item, created = self.cart_items.get_or_create(color_variant=color_variant)
        cart_item.quantity += quantity
        cart_item.save()

    def place_order(self):
        """Finalize the order, ensuring no over-ordering of stock."""
        # First check if cart has items
        if not self.cart_items.exists():
            raise ValidationError("Cannot place order for empty cart")
            
        # Check if order already exists
        if hasattr(self, 'order'):
            raise ValidationError("Order already exists for this cart")
            
        for cart_item in self.cart_items.all():
            color_variant = cart_item.color_variant
            quantity = cart_item.quantity

            # Validate stock
            current_stock = color_variant.total_quantity
            if quantity > current_stock:
                raise ValidationError(
                    f"Cannot place order for {quantity} items of {color_variant}. Only {current_stock} available."
                )
            
            # Deduct stock
            color_variant.total_quantity -= quantity
            color_variant.save()
        
        # Create order
        order = Order.objects.create(cart=self)
        
        # Create order items
        for cart_item in self.cart_items.all():
            OrderItem.objects.create(
                order=order,
                color_variant=cart_item.color_variant,
                quantity=cart_item.quantity
            )
        
        return order

@receiver(post_save, sender=Cart)
def handle_paid_cart(sender, instance, created, **kwargs):
    """Create order when cart is marked as paid"""
    if not created and instance.is_paid:
        try:
            # Check if order doesn't exist yet
            if not hasattr(instance, 'order'):
                instance.place_order()
        except ValidationError:
            # If order creation fails, revert is_paid status
            Cart.objects.filter(id=instance.id).update(is_paid=False)

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'color_variant')

    def __str__(self):
        return f"{self.quantity}x {self.color_variant}"
    
    def get_item_price(self):
        return (self.color_variant.final_price()) * self.quantity
    
    def validate_quantity(self):
        """Ensure quantity doesn't exceed available stock"""
        if self.quantity > self.color_variant.total_quantity:
            self.quantity = self.color_variant.total_quantity

    def save(self, *args, **kwargs):
        """Override save to include quantity validation"""
        self.validate_quantity()
        super().save(*args, **kwargs)


class Payment(BaseModel):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('failed', 'Failed'),
        ('succeeded', 'Succeeded'),
    ]
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='payment')
    stripe_payment_intent_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

class Order(BaseModel):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name="order")
    created_at = models.DateTimeField(auto_now_add=True)
    is_shipped = models.BooleanField(default=False)

    

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.color_variant} in Order #{self.order.id}"

class Wishlist(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="wishlists")
    color_variants = models.ManyToManyField(ColorVariant, through='WishlistItem')

    def __str__(self):
        return f"Wishlist for {self.owner.user.username}"

    @property
    def total_items(self):
        return self.wishlist_items.count()

class WishlistItem(BaseModel):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="wishlist_items")
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wishlist', 'color_variant')

    def __str__(self):
        return f"{self.color_variant} in {self.wishlist.owner.user.username}'s wishlist"

class Feedback(BaseModel):
    commentator =models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="commentators")
    comment = models.TextField()
    product = models.ForeignKey(ColorVariant, on_delete=models.CASCADE, related_name="product_feedbacks")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback by {self.commentator.user.username} on {self.product.color_name}"