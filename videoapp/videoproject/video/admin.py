from django.contrib import admin
from .models import Video, Comment, News, Contact

# Register your models here.
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(News)
admin.site.register(Contact)