from django.shortcuts import redirect, render
from .models import Video
from .models import Video
from .models import News 
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Contact
from datetime import datetime
from user.models import CustomUser
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.response import Response
# from .serializers import VideoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

# Create your views here.
# @login_required
# def get(request):
#     post = Video.objects.all()
#     return render(request, 'service.html',{'videos': post})
# class GetVideo(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = VideoSerializer    
#     def get(self, request, pk=None, format=None):
#         id=pk
#         if id is not None:
#             try:
#                 post=Video.objects.get(id=id)
#                 serializer = VideoSerializer(post)
#                 return Response(serializer.data)
#             except Video.DoesNotExist:
#                 return Response({"msg":"Video doesnot exist!"}, status=status.HTTP_404_NOT_FOUND)
                    
#         post = Video.objects.all()
#         serializer = VideoSerializer(post, many=True)
#         # return Response(serializer.data)
#         return render(request, 'service.html',{'videos': post})

def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email , password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            # request.session.save()
            return render(request,"index.html")
        else:
            messages.error(request,"Bad request")
            return redirect(signin)
    return render(request, "signin.html")
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        myuser = CustomUser.objects.create_user(username=username,email=email, password=password)
        myuser.email = email
        myuser.save()

        messages.success(request, "Registration Success!")
        return redirect(signin)
    # message={"hello":"welcome"}
    return render(request, "signup.html")

@login_required
def index(request):

    # from datetime import datetime
    
    # current_hour = datetime.now().hour
    # if current_hour < 12:
    #     greeting = "Good morning"
    # elif 12 <= current_hour < 18:
    #     greeting = "Good afternoon"
    # else:
    #     greeting = "Good evening"
    
    # context = {
    #     "welcome_message": f"{greeting}, {request.user.username}!",
    #     "user": request.user
    # }

    my_dict = {
        "insert_me":"Hello! I am from views.py",
        "insert_me":"Hello! I am from views.py",
        "insert_me":"Hello! I am from views.py",
        "user":request.user.username,

        }
    messages.success(request, f"Welcome to Bishok Multimedia, {request.user.username}!")
    
   # return HttpResponse("this is home page")
    return render(request,'index.html', my_dict)

@login_required
def about(request):
    about_list = News.objects.all()
    return render(request, 'about.html', {'about_list': about_list})
    #return HttpResponse("this is about page")

@login_required
def contact(request):
    #return HttpResponse("this is contact page")
    if request.method =="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact(name = name, email=email, phone=phone, message=message, date=datetime.today())
        contact.save()
        messages.success(request,'Message has bees Sent!')
    return render(request,'contact.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out successfully!")
    return render(request,'signin.html')

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Video
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required
def video_list(request):
    videos = Video.objects.all()
    return render(request, 'service.html', {'videos': videos})
@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user = request.user
    if user.is_authenticated:
        if user in video.disliked_by.all():
            video.disliked_by.remove(user)
            video.dislikes -= 1
        if user not in video.liked_by.all():
            video.liked_by.add(user)
            video.likes += 1
        else:
            video.liked_by.remove(user)
            video.likes -= 1
        video.save()
    return JsonResponse({'likes': video.likes, 'dislikes': video.dislikes})
@login_required
def dislike_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user = request.user
    if user.is_authenticated:
        if user in video.liked_by.all():
            video.liked_by.remove(user)
            video.likes -= 1
        if user not in video.disliked_by.all():
            video.disliked_by.add(user)
            video.dislikes += 1
        else:
            video.disliked_by.remove(user)
            video.dislikes -= 1
        video.save()
    return JsonResponse({'likes': video.likes, 'dislikes': video.dislikes})