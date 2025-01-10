from rest_framework import serializers
from .models import Feedback, Category, Product, SizeVariant, ColorVariant, CartItem, Cart, Payment, Wishlist, WishlistItem

class ColorVariantSerializer(serializers.ModelSerializer):
    price = serializers.ReadOnlyField()

    class Meta:
        model = ColorVariant
        fields = '__all__'

class SizeVariantSerializer(serializers.ModelSerializer):
    product_colors = ColorVariantSerializer(many=True)

    class Meta:
        model = SizeVariant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    product_sizes = SizeVariantSerializer(many=True, read_only=True)
    product_colors = ColorVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='color_variant.size.product.product_name', read_only=True)
    size = serializers.CharField(source='color_variant.size.size_name', read_only=True)
    color = serializers.CharField(source='color_variant.color_name', read_only=True)
    
    item_price = serializers.DecimalField(source='color_variant.final_price', max_digits=10, decimal_places=2, read_only=True)
    total_item_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id', 'product_name','size','color', 'color_variant','quantity','item_price', 'total_item_price']
        read_only_fields = ['cart']
    def get_total_item_price(self, obj):
        return obj.get_item_price()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cart_items', many=True, read_only=True)
    cart_owner = serializers.CharField(source='cart_owner.user.username', read_only=True)
    total_cart_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'cart_owner', 'is_paid', 'total_cart_price','items','total_items']

    def get_total_cart_price(self, obj):
        return obj.get_cart_total()
    
    def get_total_items(self, obj):
        return obj.get_total_items()

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ['id', 'color_variant', 'added_date']
        read_only_fields = ['added_date']

class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(source='wishlist_items', many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'items', 'total_items']

class FeedbackSerializer(serializers.ModelSerializer):
    commentator_name = serializers.CharField(source='commentator.user.username', read_only=True)
    product_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Feedback
        fields = ['id', 'commentator_name','product','product_details' ,'rating', 'comment', 'created_at']
        # read_only_fields = ['commentator','product_name']

    def get_product_details(self, obj):
        product = obj.product  
        return {
            "color_name": product.color_name,
            "size_name": product.size.size_name,
            "product_name": product.size.product.product_name,
            # "final_price": product.final_price(),
        }