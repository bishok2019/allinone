from django.contrib import admin
from django.urls import path
from api import views
urlpatterns = [
    path('api/',views.VideoList.as_view()),
    # path('api/<int:pk>',views.VideoApi)
]