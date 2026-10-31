from django.contrib import admin, messages
from .models import *


# admin.site.register(
#     [
#             Channel, Category, Video, Playlist, PlaylistVideos,
#             Like, Watchs, Comment, Following
#         ]
#     )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'created_at'
    ]
    list_display_links = ['name']
    ordering = ['-created_at']
    list_per_page = 20
    search_fields = ['name']


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'title', 'created_at'
    ]
    list_display_links = ['user']
    list_editable = ['title']
    ordering = ['-created_at']
    list_per_page = 20
    search_fields = ['title', 'user']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = [
        'channel', 'title', 'category', 'type', 'created_at'
    ]
    list_display_links = ['channel']
    list_editable = ['title', 'category', 'type']
    ordering = ['-created_at']
    list_per_page = 20
    list_filter = ['category', 'type']
    search_fields = ['title', 'channel', 'category']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = [
        'channel', 'title', 'created_at'
    ]
    list_display_links = ['channel']
    list_editable = ['title']
    ordering = ['-created_at']
    list_per_page = 20
    search_fields = ['title', 'channel']


@admin.register(PlaylistVideos)
class PlaylistVideosAdmin(admin.ModelAdmin):
    list_display = [
        'playlist', 'video', 'created_at'
    ]
    list_display_links = ['playlist', 'video']
    ordering = ['-created_at']
    list_per_page = 20
    search_fields = ['video', 'playlist']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'video', 'created_at'
    ]
    list_display_links = ['user', 'video']
    ordering = ['-created_at']
    list_per_page = 20
    search_fields = ['video', 'user']


@admin.register(Watchs)
class WatchsAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'video', 'created_at'
    ]
    list_display_links = ['user', 'video']
    ordering = ['-created_at']
    list_per_page = 20
    search_fields = ['video', 'user']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'video', 'created_at'
    ]
    list_display_links = ['user', 'video']
    ordering = ['-created_at']
    list_per_page = 20
    search_fields = ['video', 'user', 'comment']


@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'channel', 'created_at'
    ]
    list_display_links = ['user', 'channel']
    ordering = ['-created_at']
    list_per_page = 20
    search_fields = ['video', 'channel']
