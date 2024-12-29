from django.contrib import admin
from .models import Video, Comment, News, Contact

# Register your models here.
admin.site.register(Contact)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Video)