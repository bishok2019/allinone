from django.urls import path
from .views import index
from products.views import get_product
urlpatterns=[
    path('', index, name='home'),
    path('product/<slug:slug>', get_product, name='get_product'),
]