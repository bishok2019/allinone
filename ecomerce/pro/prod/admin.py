from django.contrib import admin
from nested_admin import NestedTabularInline, NestedModelAdmin
from .models import Product, ProductSize, SizeColor

# Nested Admin for creating products
class SizeColorInline(NestedTabularInline):
    model = SizeColor
    extra = 1  # Number of empty forms to display by default

class ProductSizeInline(NestedTabularInline):
    model = ProductSize
    extra = 1
    inlines = [SizeColorInline]  # Embedding SizeColor inline within ProductSize

@admin.register(Product)
class ProductAdmin(NestedModelAdmin):
    inlines = [ProductSizeInline]  # Embedding ProductSize inline within Product


# Separate Admin for ProductSize
@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'price']
    list_filter = ['product']
    search_fields = ['name', 'product__name']
    inlines = []  # No inlines because we manage colors separately


# Separate Admin for SizeColor
@admin.register(SizeColor)
class SizeColorAdmin(admin.ModelAdmin):
    list_display = ['get_product', 'get_size', 'name', 'price', 'get_final_price']
    list_filter = ['product_size__product', 'product_size__name']
    search_fields = ['name', 'product_size__product__name']

    def get_product(self, obj):
        return obj.product_size.product.name
    get_product.short_description = 'Product'
    
    def get_size(self, obj):
        return obj.product_size.name
    get_size.short_description = 'Size'
    
    def get_final_price(self, obj):
        return obj.final_price()
    get_final_price.short_description = 'Final Price'



# from django.contrib import admin
# from nested_admin import NestedTabularInline, NestedModelAdmin
# from .models import Product, ProductSize, SizeColor

# class SizeColorInline(NestedTabularInline):
#     model = SizeColor
#     extra = 1  # Number of empty forms to display by default

# class ProductSizeInline(NestedTabularInline):
#     model = ProductSize
#     extra = 1
#     inlines = [SizeColorInline]  # Embedding SizeColor inline within ProductSize

# @admin.register(Product)
# class ProductAdmin(NestedModelAdmin):
#     inlines = [ProductSizeInline]  # Embedding ProductSize inline within Product




# from django.contrib import admin
# from .models import Product, ProductSize, SizeColor

# class ProductSizeInline(admin.TabularInline):
#     model = ProductSize
#     extra = 1  # Number of empty forms to display

# class SizeColorInline(admin.TabularInline):
#     model = SizeColor
#     extra = 1

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'base_price']
#     search_fields = ['name']
#     inlines = [ProductSizeInline]

# @admin.register(ProductSize)
# class ProductSizeAdmin(admin.ModelAdmin):
#     list_display = ['product', 'name', 'price']
#     list_filter = ['product']
#     search_fields = ['name', 'product__name']
#     inlines = [SizeColorInline]

# @admin.register(SizeColor)
# class SizeColorAdmin(admin.ModelAdmin):
#     list_display = ['get_product', 'get_size', 'name', 'price', 'get_final_price']
#     list_filter = ['product_size__product', 'product_size__name']
#     search_fields = ['name', 'product_size__product__name']

#     def get_product(self, obj):
#         return obj.product_size.product.name
#     get_product.short_description = 'Product'
    
#     def get_size(self, obj):
#         return obj.product_size.name
#     get_size.short_description = 'Size'
    
#     def get_final_price(self, obj):
#         return obj.final_price()
#     get_final_price.short_description = 'Final Price'