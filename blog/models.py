from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author     = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:40]

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.count()


class PostMedia(models.Model):
    post  = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='media_files'
    )
    file  = models.FileField(upload_to='posts/media/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def is_video(self):
        return self.file.name.lower().endswith('.mp4')

    def is_image(self):
        return any(
            self.file.name.lower().endswith(ext)
            for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        )

    def __str__(self):
        return f"Media {self.id} for post {self.post_id}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['post', 'user']

    def __str__(self):
        return f"{self.user} liked post {self.post_id}"


class Comment(models.Model):
    post       = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    parent     = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='replies'
    )
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.text[:30]
