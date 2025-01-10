from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Product, SizeVariant,Feedback, ColorVariant, Cart, CartItem, Order, OrderItem, Payment, Wishlist, WishlistItem
from django.utils.html import format_html

admin.site.register(Payment)
admin.site.register(WishlistItem)
admin.site.register(Wishlist)
# Inline models to display CartItem in the Cart Admin page
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ('color_variant', 'quantity', 'get_item_price')
    fields = ('color_variant', 'quantity', 'get_item_price')
    
    def get_item_price(self, obj):
        return obj.get_item_price()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'category_image')
    prepopulated_fields = {'slug': ('category_name',)}

    def category_image_preview(self, obj):
        if obj.category_image:
            return format_html('<img src="{}" style="max-width:100px;max-height:100px;"/>', obj.category_image.url)
        return "-"
    category_image_preview.short_description = _("Category Image Preview")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'base_price', 'slug')
    search_fields = ('product_name', 'category__category_name',)
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('product_name',)}


@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ('size_name', 'product', 'additional_price')
    list_filter = ('product',)


@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ('color_name', 'size', 'get_product', 'total_quantity', 'final_price')
    list_filter = ('size', 'size__product',)

    def final_price(self, obj):
        return obj.final_price()
    final_price.short_description = _('Final Price')

    def get_product(self, obj):
        return obj.size.product.product_name if obj.size else None
    get_product.short_description = _('Product')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_owner', 'created_at', 'updated_at', 'is_paid', 'get_total_items', 'get_cart_total')
    list_filter = ('is_paid',)
    search_fields = ('cart_owner__user__username',)

    def get_cart_total(self, obj):
        return obj.get_cart_total()
    get_cart_total.short_description = _("Total Price")

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = _("Total Items")

    def save_model(self, request, obj, form, change):
        # Automatically create order when cart is marked as paid
        if obj.is_paid:
            obj.place_order()
        super().save_model(request, obj, form, change)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'color_variant', 'quantity', 'get_item_price')
    list_filter = ('cart', 'color_variant',)

    def get_item_price(self, obj):
        return obj.get_item_price()
    get_item_price.short_description = _('Item Price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('cart', 'created_at', 'is_shipped')
    list_filter = ('is_shipped',)
    search_fields = ('cart__cart_owner__user__username',)


# @admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'color_variant', 'quantity')
    list_filter = ('order', 'color_variant',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('commentator', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__user__username', 'product__product_name')