from django.urls import path
from .views import get_product,FeedbackView, ProductApi, CartItemView, CartView, PaymentCancelView, PaymentSuccessView, PaymentView, stripe_webhook, WishlistItemView, WishlistView

urlpatterns=[
    path('<slug>/', get_product, name='get-product'),
    path('api/prod/', ProductApi.as_view()),
    path('api/prod/<int:pk>', ProductApi.as_view()),
    
    # path('api/prod/cat/', CategoryApi.as_view()),
    # path('api/prod/<uuid:pk>/', ProductApi.as_view()),

    path('api/cart/', CartView.as_view(), name='cart'),
    path('api/cart/<int:id>', CartView.as_view(), name='cart'),
    
    path('api/cart/<int:cart_id>/item/', CartItemView.as_view(), name='list_cart_items'),
    path('api/cart/<int:cart_id>/item/<int:item_id>/', CartItemView.as_view(), name='detail_cart_item'),

    path('payment/create-checkout-session/', PaymentView.as_view(),name='create-checkout-session'),
    path('payment/create-checkout-session/success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('payment/create-checkout-session/cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
    # path('webhook/stripe', StripeWebHookView.as_view(), name='stripe-webhook'),
    path('webhook/stripe', stripe_webhook, name='stripe-webhook'),

    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/items/', WishlistItemView.as_view(), name='wishlist-add'),
    path('wishlist/items/<int:pk>/', WishlistItemView.as_view(), name='wishlist-remove'),
    path('api/feedback/', FeedbackView.as_view(), name='feedback'),


]