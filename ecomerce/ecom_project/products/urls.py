from django.urls import path
from .views import get_product,ProductApi, CartItemView, CartView

urlpatterns=[
    path('<slug>/', get_product, name='get-product'),
    path('api/prod/', ProductApi.as_view()),
    # path('api/prod/cat/', CategoryApi.as_view()),
    path('api/prod/<uuid:pk>/', ProductApi.as_view()),

    path('api/cart/', CartView.as_view(), name='cart'),
    path('api/cart/<int:id>', CartView.as_view(), name='cart'),
    
    path('api/cartitem/', CartItemView.as_view(), name='cart-item'),
    path('api/cartitem/<int:id>', CartItemView.as_view(), name='cart-item'),
]