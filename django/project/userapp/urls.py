from userapp.views import ResetPasswordView, RegsiterUserView, LoginUserView, UserProfileView,ChangeUserPasswordView, SendPasswordResetEmailView
from django.urls import path

urlpatterns = [
    path('', RegsiterUserView.as_view(), name='user-register'),
    path('login', LoginUserView.as_view(), name='user-login'),
    path('profile', UserProfileView.as_view(), name='user-profile-view'),
    path('changepassword', ChangeUserPasswordView.as_view(), name='change-user-password'),
    path('send-reset-password-email', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', ResetPasswordView.as_view(), name='reset-password'),

]