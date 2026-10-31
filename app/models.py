from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Channel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='channel')
    avatar = models.FileField(upload_to='avatars/', default='avatars/ArzonYob.jpg')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.user.username}'


class Video(models.Model):
    TYPE = (
        ('video', 'Video'),
        ('shorts', 'Shorts')
    )

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_videos')
    file = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(choices=TYPE, default='video', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.title} - {self.channel.title}'


class Playlist(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='channel_playlists')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.title} - {self.channel.title}'


class PlaylistVideos(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='playlist_videos')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_playlists')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('playlist', 'video')
    
    def __str__(self):
        return f'{self.video.title} - {self.playlist.title}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_videos')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')
    
    def __str__(self):
        return f'{self.video.title} - {self.user.username}'


class Watchs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watched_videos')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_watchs')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')
    
    def __str__(self):
        return f'{self.video.title} - {self.user.username}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commented_videos')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.video.title} - {self.user.username}'


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_channels')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='channel_followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'channel')
    
    def __str__(self):
        return f'{self.channel.title} - {self.user.username}'
