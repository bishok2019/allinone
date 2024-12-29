from blogapp.views import BlogModify, BlogApi
from django.urls import path,include

urlpatterns=[
    path('', BlogApi.as_view()),
    # path('blogmodify/', views.BlogModify.as_view()),
    path('<int:pk>/', BlogModify.as_view()),
    path('api-auth/', include('rest_framework.urls')),

]