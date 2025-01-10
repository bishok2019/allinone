from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from products.models import Feedback, Product, Category, CartItem, Cart, Payment, WishlistItem, Wishlist
from .serializers import FeedbackSerializer, ProductSerializer, SizeVariantSerializer, CartSerializer, CartItemSerializer, PaymentSerializer, WishlistItemSerializer, WishlistSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import IntegrityError
from django.conf import settings
import stripe
from base.emails import send_payment_confirmation_email

def get_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Get user's wishlist items if authenticated
    user_wishlist_items = []
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(owner=request.user.profile).first()
        if wishlist:
            user_wishlist_items = list(wishlist.wishlist_items.values_list(
                'color_variant_id', flat=True
            ))

    context = {
        'product': product,
        'user_wishlist_items': user_wishlist_items,
    }
    return render(request, 'products/product.html', context)

class ProductApi(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    def get(self, request,pk=None,format=None):
        if pk is not None:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
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

    def get(self, request, id=None, format=None):
        """
        Retrieve or create the user's cart.
        """
        if id:
            try:
                cart = Cart.objects.get(id=id, cart_owner=request.user.profile)
                serializer = self.serializer_class(cart)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Cart.DoesNotExist:
                return Response({"error": "Cart not found."})
            
        cart = Cart.objects.filter(cart_owner=request.user.profile)
        if not cart:
            new_cart = Cart.objects.create(cart_owner=request.user.profile, is_paid=False) 
            serializer = CartSerializer(new_cart)
            return Response({"msg": "No carts found. A new cart has been created.","data": serializer.data}, status=status.HTTP_201_CREATED)
        serializer = self.serializer_class(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request,pk=None, format=None):
        """
        Delete the user's cart and its items.
        """
        try:
            cart = Cart.objects.get(id=pk, cart_owner=request.user.profile)
            cart.delete()
            return Response({"msg": "Cart deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND)

class CartItemView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    
    def get(self, request, cart_id, item_id=None, format=None):
        
        try:
            cart = Cart.objects.get(id=cart_id, cart_owner=request.user.profile)

            if item_id:
                cart_item = CartItem.objects.get(id=item_id, cart=cart)
                serializer = CartItemSerializer(cart_item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                cart_items = CartItem.objects.filter(cart=cart)
                serializer = CartItemSerializer(cart_items, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request, format=None):
        cart = Cart.objects.filter(cart_owner = request.user.profile, is_paid=False).last()
        if not cart:
            cart, created = Cart.objects.get_or_create(cart_owner=request.user.profile, is_paid=False)
            print("New Cart Added for user")
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(cart=cart)
                return Response({"msg": "Item added to cart", "data" : serializer.data},status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error":"This item already exists in your cart. Try updating the existing item if you want more."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, cart_id, item_id, format=None):
        """
        Update an item in a specific cart.
        """
        try:
            cart = Cart.objects.get(id=cart_id, cart_owner=request.user.profile)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, cart_id, item_id, format=None):
        """
        Remove an item from a specific cart.
        """
        try:
            # Fetch the cart and item
            cart = Cart.objects.get(id=cart_id, cart_owner=request.user.profile)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)

            # Delete the item
            cart_item.delete()
            return Response({"msg": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)

        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)
        
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


from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
stripe.api_key = settings.STRIPE_SECRET_KEY
class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            cart_id = request.data.get('cart_id')
            cart = Cart.objects.get(id=cart_id)

            if cart.is_paid:
                return Response({"error":"Cart is already paid"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not cart.cart_items.exists():
                return Response({"error":"Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

            line_items = []
            for item in cart.cart_items.all():
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(item.color_variant.final_price() * 100),
                        'product_data': {
                            'name': str(item.color_variant),
                        },
                    },
                    'quantity': item.quantity,
                })

            # Create checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri('success/'),
                cancel_url=request.build_absolute_uri('cancel/'),
                metadata={
                    'cart_id': str(cart.id),
                },
                payment_intent_data={
                    'setup_future_usage': 'off_session',
                    'metadata': {
                        'cart_id': str(cart.id),
                        'user_id': str(request.user.username)
                    }
                }
            )
            print(checkout_session.payment_intent)
            print(checkout_session)

            # Create Payment object with pending status
            payment = Payment.objects.create(
                cart=cart,
                status='pending',
                stripe_payment_intent_id=checkout_session.payment_intent or ''  # Handle null case
            )

            
            return Response({
                'session_id': checkout_session.id,
                'checkout_url': checkout_session.url
            })
        
        except Cart.DoesNotExist:
            return Response(
                {"error":"Cart not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except stripe.error.StripeError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"Unexpected error in PaymentView: {str(e)}")  # Log unexpected errors
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        print(f"Invalid payload error: {str(e)}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f"Invalid signature error: {str(e)}")
        return HttpResponse(status=400)

    try:
        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # print(f"line 249:event->{event}")
            
            # Get cart_id from metadata
            cart_id = session.get('metadata', {}).get('cart_id')
            if not cart_id:
                print("No cart_id in metadata")
                return HttpResponse(status=400)

            # Get or create payment for this cart
            cart = Cart.objects.get(id=cart_id)
            payment, created = Payment.objects.get_or_create(
                cart=cart,
                defaults={'status': 'pending', 'stripe_payment_intent_id': session.payment_intent or ''}
            )

            # Update payment status
            payment.status = 'processing'
            if session.payment_intent:
                payment.stripe_payment_intent_id = session.payment_intent
            payment.save()

            # Mark cart as paid
            cart.is_paid = True
            cart.save()

            # Send payment confirmation email
            send_payment_confirmation_email(
                email=cart.cart_owner.user.email,
                cart = cart,
                total_amount=cart.get_cart_total()
            )

        # Handle payment_intent.succeeded event
        elif event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            try:
                # Try to find payment by payment intent ID
                payment = Payment.objects.get(stripe_payment_intent_id=payment_intent.id)
                payment.status = 'succeeded'
                payment.save()
                
            except Payment.DoesNotExist:
                # If not found, try to find by cart_id in metadata
                cart_id = payment_intent.get('metadata', {}).get('cart_id')
                if cart_id:
                    cart = Cart.objects.get(id=cart_id)
                    payment = Payment.objects.get(cart=cart)
                    payment.stripe_payment_intent_id = payment_intent.id
                    payment.status = 'succeeded'
                    payment.save()

        # Handle payment_intent.payment_failed event
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent.id)
            payment.status = 'failed'
            payment.save()
            
            # Update cart status
            cart = payment.cart
            cart.is_paid = False
            cart.save()
            

    except (Cart.DoesNotExist, Payment.DoesNotExist) as e:
        print(f"Database object not found: {str(e)}")
        return HttpResponse(status=404)
    except Exception as e:
        print(f"Unexpected error in webhook: {str(e)}")
        return HttpResponse(status=500)

    return HttpResponse(status=200)


class PaymentSuccessView(APIView):
    def get(self, request):
        return Response({'status':'Payment successfull'})

class PaymentCancelView(APIView):
    def get(self, request):
        return Response({'status': 'Payment cancelled'})
    
class WishlistView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer
    
    def get(self, request):
        """Retrieve user's wishlist"""
        wishlist, created = Wishlist.objects.get_or_create(owner=request.user.profile)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

class WishlistItemView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistItemSerializer
    
    def post(self, request):
        """Add item to wishlist"""
        wishlist, created = Wishlist.objects.get_or_create(owner=request.user.profile)
        
        serializer = WishlistItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(wishlist=wishlist)
                return Response({
                    "message": "Item added to wishlist",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({
                    "error": "This item is already in your wishlist"
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Remove item from wishlist"""
        try:
            wishlist = Wishlist.objects.get(owner=request.user.profile)
            item = WishlistItem.objects.get(pk=pk, wishlist=wishlist)
            item.delete()
            return Response({
                "message": "Item removed from wishlist"
            }, status=status.HTTP_204_NO_CONTENT)
        except (Wishlist.DoesNotExist, WishlistItem.DoesNotExist):
            return Response({
                "error": "Item not found"
            }, status=status.HTTP_404_NOT_FOUND)

class FeedbackView(APIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request,pk=None,format=None):
        if pk is not None:
            feedback = Feedback.objects.get(pk=pk)
            serializer = FeedbackSerializer(feedback)
            return Response(serializer.data)
        else:
            feedback = Feedback.objects.all()
            serializer = FeedbackSerializer(feedback,many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
       serializer = FeedbackSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save(commentator=request.user.profile)
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)