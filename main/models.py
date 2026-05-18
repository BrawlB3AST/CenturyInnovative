from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    author = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='main_posts')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class PostMedia(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='media_files'
    )

    file = models.FileField(upload_to='posts/media/')

    def is_video(self):
        return self.file.url.endswith('.mp4')

    def is_image(self):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        return any(self.file.url.lower().endswith(ext) for ext in image_extensions)
    
    
class Profile(models.Model):
    user      = models.OneToOneField(User, on_delete=models.CASCADE)
    bio       = models.TextField(blank=True)
    avatar_initial_color = models.CharField(max_length=7, default='#ff4d6d')  # hex color
    website   = models.URLField(blank=True)
    twitter   = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def post_count(self):
        return Post.objects.filter(author=self.user).count()