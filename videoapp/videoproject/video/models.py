from django.db import models
from django.conf import settings

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    phone = models.CharField(max_length=50)
    message = models.TextField()
    date = models.DateField()
    def __str__(self):
        return self.name
    

class News(models.Model):
    news_title = models.CharField(max_length=100)
    news_desc = models.CharField(max_length=100)
    news_image = models.FileField(upload_to="news/", max_length=250, null=True, default=None)

class Video(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_videos', blank=True)
    disliked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_videos', blank=True)
    def __str__(self):
        return self.title

class Comment(models.Model):
    video = models.ForeignKey(Video, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"
