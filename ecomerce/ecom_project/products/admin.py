# from django.contrib import admin
# from .models import Category, Product, ProductImage, SizeVariant, ColorVariant, ProductColorImage


# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 1
#     fields = ['image']
#     verbose_name = "Product Image"
#     verbose_name_plural = "Product Images"


# class ProductColorImageInline(admin.TabularInline):
#     model = ProductColorImage
#     extra = 1
#     fields = ['product_color_image']
#     verbose_name = "Product Color Image"
#     verbose_name_plural = "Product Color Images"


# class ColorVariantInline(admin.TabularInline):
#     model = ColorVariant
#     extra = 1
#     fields = ['color_name', 'additional_price']
#     verbose_name = "Color Variant"
#     verbose_name_plural = "Color Variants"
#     inlines = [ProductColorImageInline]


# class SizeVariantInline(admin.TabularInline):
#     model = SizeVariant
#     extra = 1
#     fields = ['size_name', 'additional_price']
#     verbose_name = "Size Variant"
#     verbose_name_plural = "Size Variants"


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['product_name', 'category', 'base_price', 'slug']
#     search_fields = ['product_name', 'category__category_name']
#     list_filter = ['category']
#     prepopulated_fields = {'slug': ('product_name',)}

#     # Define the inlines that are directly related to Product
#     inlines = [
#         ProductImageInline,
#         SizeVariantInline,  # Only SizeVariant is directly related to Product
#     ]


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['category_name', 'slug']
#     search_fields = ['category_name']
#     prepopulated_fields = {'slug': ('category_name',)}


# admin.site.register(ProductImage)
# admin.site.register(SizeVariant)
# admin.site.register(ColorVariant)
# admin.site.register(ProductColorImage)


##################################################
##################################################
##################################################
from django.contrib import admin
import nested_admin
from .models import Category, Product, ProductImage, SizeVariant, ColorVariant, ProductColorImage

class ProductColorImageInline(nested_admin.NestedTabularInline):
    model = ProductColorImage
    extra = 1

class ColorVariantInline(nested_admin.NestedStackedInline):
    model = ColorVariant
    inlines = [ProductColorImageInline]
    extra = 1

class SizeVariantInline(nested_admin.NestedStackedInline):
    model = SizeVariant
    inlines = [ColorVariantInline]
    extra = 1

class ProductImageInline(nested_admin.NestedTabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(nested_admin.NestedModelAdmin):
    list_display = ('product_name', 'category', 'base_price', 'slug')
    search_fields = ('product_name', 'category__category_name')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductImageInline, SizeVariantInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)


####
# admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(SizeVariant)
admin.site.register(ColorVariant)
admin.site.register(ProductColorImage)