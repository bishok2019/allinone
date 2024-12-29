from rest_framework import serializers
from multiapp.models import Video, Contact, Comment

class VideoSerializer(serializers.ModelSerializer):
    
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'created_at', 'updated_at','author_email','file','likes', 'dislikes']
        read_only_fields = ['author', 'likes', 'dislikes', 'created_at', 'updated_at']
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'