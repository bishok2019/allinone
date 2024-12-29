from django.urls import path
from accounts.views import login, register, activate_email

urlpatterns =[
    path('login/' , login, name="login" ),
    path('register/' , register, name="register" ),
    path('activate/<email_token>',activate_email, name="activate_email")
]