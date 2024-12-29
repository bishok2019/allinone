"""
URL configuration for videoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from video import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('service', views.video_list, name='video_list'),
    path('like/<int:video_id>/', views.like_video, name='like_video'),
    path('dislike/<int:video_id>/', views.dislike_video, name='dislike_video'),
   
    path('admin/', admin.site.urls),
    path("", views.index, name='home'),
    # path("service", views.GetVideo.as_view()),
    # path("service", views.get, name='get'),
    path("contact", views.contact, name='contact'),
    path("about", views.about, name='about'),
    path("signup", views.signup, name='signup'),
    path("signin", views.signin, name='signin'),
    path("signout", views.signout, name='signout')
    # path('signin/', include('rest_framework.urls')),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)