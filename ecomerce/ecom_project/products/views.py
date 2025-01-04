from django.shortcuts import render,get_object_or_404
from products.models import Product, Category, CartItem, Cart
from .serializers import ProductSerializer, SizeVariantSerializer, CartSerializer, CartItemSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import IntegrityError
    
def get_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product,
    }
    return render(request, 'products/product.html', context)

class ProductApi(APIView):
    
    serializer_class = ProductSerializer
    permission_class = [IsAuthenticated,IsAdminUser]
    def get(self, request,pk=None,format=None):
        if pk is not None:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        product = Product.objects.all()
        serializer = ProductSerializer(many=True)
        return Response(serializer.data)
    
    def post(self, request, pk=None, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get(self, request, format=None):
        """
        Retrieve or create the user's cart.
        """
        cart, created = Cart.objects.get_or_create(cart_owner=request.user.profile)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        """
        Delete the user's cart and its items.
        """
        try:
            cart = Cart.objects.get(cart_owner=request.user.profile)
            cart.delete()
            return Response({"msg": "Cart deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND)

class CartItemView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get(self, request,pk=None, format=None):
        """
        Retrieve or create the user's cart.
        """
        cart = Cart.objects.get(cart_owner=request.user.profile)
        # if id is not None:
        items = cart.cart_items.all()
        serializer = self.serializer_class(items, many=True)
            # serializer = CartItemSerializer(cart, many=True) # Cart obj is not iterable
        return Response(serializer.data, status=status.HTTP_200_OK)
        # items = cart.cart_items.all(id=pk)
        # serializer = self.serializer_class(items, many=True)
        # return Response(serializer.data)

    def post(self, request, format=None):
        """
        Add an item to the user's cart.
        """
        # Get or create a cart for the authenticated user
        cart, created = Cart.objects.get_or_create(cart_owner=request.user.profile)

        if created:
            
            print(f"New cart created for user: {request.user.username}")

        # try:
        #     # Ensure the user has a cart
        #     cart = Cart.objects.get(cart_owner=request.user.profile)
        # except Cart.DoesNotExist:
        #     return Response({"error": "Cart does not exist. Create a cart first."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            
            try:
                serializer.save(cart=cart)
                return Response({"msg": "Item added to cart", "data" : serializer.data},status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error":"This item already exists in your cart. Try updating the existing item if you want more."}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        """
        Remove an item from the user's cart.
        """
        try:
            cart = Cart.objects.get(cart_owner=request.user.profile)
            cart_item = CartItem.objects.get(pk=pk, cart=cart)
            cart_item.delete()
            return Response({"msg": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({"error": "Item or Cart not found"}, status=status.HTTP_404_NOT_FOUND)

# class CategoryApi(APIView):
#     serializer_class = CategorySerializer
#     def get(self, request,pk=None,format=None):
#         if pk is not None:
#             category = Category.objects.get(pk=pk)
#             serializer = CategorySerializer(category)
#             return Response(serializer.data)
#         category = Category.objects.all()
#         serializer = CategorySerializer(category, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, pk=None, format=None):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

