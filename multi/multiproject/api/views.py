from django.shortcuts import render
from multiapp.models import Video
from .serializers import VideoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
# Create your views here.

class VideoList(ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def VideoApi(request, pk=None):
#     if request.method == 'GET':
#         if pk is not None:
#             video = Video.objects.get(id=pk)
#             serializer = VideoSerializer(video)
#             return Response(serializer.data)
#         video= Video.objects.all()
#         serializer = VideoSerializer(video, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = VideoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
    
#     if request.method == 'PUT':
#         id = request.data.get('id')
#         video = Video.objects.get(pk=id)
#         serializer = VideoSerializer(video, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,{'msg':'Complete data updated !!'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'PATCH':
#         id = request.data.get('id')
#         video = Video.objects.get(pk=id)
#         serializer = VideoSerializer(video, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,{'msg':'Partial data updated !!'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     if request.method == 'DELETE':
#         video = Video.objects.get(id=pk)
#         video.delete()
#         return Response({'msg':'Data Deleted !'})
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)