# from rest_framework.routers import DefaultRouter
# from django.urls import path, include
# from .views import VideoViewSet

# router = DefaultRouter()
# router.register(r'videos', VideoViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('videolist/', views.video_list, name='video_list'),
    path('like/<int:video_id>/', views.like_video, name='like_video'),
    path('dislike/<int:video_id>/', views.dislike_video, name='dislike_video'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('', views.index, name='home'),
]