from django.contrib import admin
from .models import Post, Like, Comment, PostMedia


admin.site.register(Post)
admin.site.register(PostMedia)
admin.site.register(Like)
admin.site.register(Comment)