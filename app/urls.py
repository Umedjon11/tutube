from django.urls import path
from .views import (
    HomeView, RegisterUserView, LoginUserView, ActivateAccountView, HistoryView,
    VideoDetailView, SubscribeView, UnsubscribeView, AddLikeView, RemoveLikeView,
    ShotsDetailView, AddLikeShortsView, RemoveLikeShortsView, MyChannelView,
    DeleteVideoView, AddVideoView, UpdateVideoView, MyPlaylistsView, DeletePlaylistView,
    AddPlaylistView, UpdatPlaylistView, PlaylistDetailView, RemoveVideoFromPlaylistView,
    AddVideoToPlaylistView, ChannelDetailViews, DeleteFromHistoryView, ChannelPlaylistDetailViews,
    LogoutUserView
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<int:category_id>/', HomeView.as_view(), name='category'),
    path('channel/', MyChannelView.as_view(), name='my_channel'),
    path('channel/<int:pk>/', ChannelDetailViews.as_view(), name='channel_info'),
    path('channel/<int:pk>/playlist/', ChannelPlaylistDetailViews.as_view(), name='channel_playlists'),
    path('channel/playlist/', MyPlaylistsView.as_view(), name='my_playlists'),
    path('channel/playlist/add/', AddPlaylistView.as_view(), name='add_playlist'),
    path('channel/playlist/<int:pk>/info/', PlaylistDetailView.as_view(), name='playlist_info'),
    path('channel/playlist/video/<int:pk>/remove/', RemoveVideoFromPlaylistView.as_view(), name='remove_from_playlist'),
    path('video/<int:video_id>/add/<int:playlist_id>/', AddVideoToPlaylistView.as_view(), name='add_to_playlist'),
    path('channel/playlist/<int:pk>/update/', UpdatPlaylistView.as_view(), name='update_playlist'),
    path('channel/playlist/<int:pk>/delete/', DeletePlaylistView.as_view(), name='delete_playlist'),
    path('video/add/', AddVideoView.as_view(), name='create_video'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path('video/<int:pk>/update/', UpdateVideoView.as_view(), name='video_edit'),
    path('video/<int:pk>/delete/', DeleteVideoView.as_view(), name='video_delete'),
    path('video/<int:pk>/like/', AddLikeView.as_view(), name='video_like'),
    path('video/<int:pk>/unlike/', RemoveLikeView.as_view(), name='video_unlike'),
    path('channel/<int:pk>/subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('channel/<int:pk>/unsubscribe/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('shorts/<int:pk>/', ShotsDetailView.as_view(), name='shorts_detail'),
    path('shorts/<int:pk>/like/', AddLikeShortsView.as_view(), name='shorts_like'),
    path('shorts/<int:pk>/unlike/', RemoveLikeShortsView.as_view(), name='shorts_unlike'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('history/', HistoryView.as_view(), name='history'),
    path('history/<int:pk>/delete/', DeleteFromHistoryView.as_view(), name='delete_from_history'),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate_account'),
]