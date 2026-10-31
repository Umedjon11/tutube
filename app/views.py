from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from .models import (
    Category, Channel, Video, Like, Watchs, Playlist, PlaylistVideos, Following, Comment
)
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.db.models import Q
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin  

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import send_mail


class HomeView(ListView):
    model = Video
    template_name = 'home.html'
    context_object_name = 'videos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()

        return context

    def get_queryset(self):
        query = super().get_queryset()
        search = self.request.GET.get('search', '')
        category_id = self.kwargs.get('category_id')

        if category_id:
            query = query.filter(category__id = category_id)

        if search:
            query = query.filter(
                Q(title__icontains = search) |
                Q(description__icontains = search)
            )
        
        return query


class RegisterUserView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()

        if user:
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)
            activate_url = self.request.build_absolute_uri(
                reverse(
                    'activate_account',
                    kwargs = {
                        'uidb64': uidb64,
                        'token': token
                    }
                )
            )

            html_message = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
              <meta charset="UTF-8">
              <title>Activation of Account YouTube</title>
            </head>
            <body style="margin: 0; padding: 40px 15px; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
              <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 540px; background-color: #ffffff; border-radius: 20px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); padding: 40px 36px;">
                <tr>
                  <td>
                    <div style="font-size: 26px; font-weight: 800; color: #02B15F; margin-bottom: 24px; letter-spacing: -0.5px;">
                      YouTube
                    </div>

                    <h1 style="margin: 0 0 16px 0; font-size: 20px; font-weight: 700; color: #0f172a; line-height: 1.3;">
                      Welcome to YouTube!
                    </h1>

                    <p style="margin: 0 0 24px 0; font-size: 15px; color: #475569; line-height: 1.5;">
                      Hello, <strong>{user.username}</strong>!<br>
                      For verify your account click to link under the text:
                    </p>

                    <div style="border: 2px dashed #cbd5e1; border-radius: 14px; background-color: #ffffff; padding: 20px; text-align: center; margin-bottom: 24px;">
                      <a href="{activate_url}" target="_blank" style="display: inline-block; background-color: #02B15F; color: #ffffff; text-decoration: none; font-size: 16px; font-weight: 600; padding: 12px 32px; border-radius: 8px;">
                        Activate Account
                      </a>
                    </div>

                    <p style="margin: 0 0 32px 0; font-size: 14px; color: #475569; line-height: 1.5;">
                      Link will works for <strong>15 minutes</strong>. If you does not registered in YouTube, just ignore this message.
                    </p>

                    <div style="text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #f1f5f9; padding-top: 20px;">
                      &copy; 2026 YouTube.
                    </div>
                  </td>
                </tr>
              </table>
            </body>
            </html>
            """

            plain_message = (
                f"Hello, {user.username}!\n\n"
                f"For activate your account click to this link:\n{activate_url}\n\n"
                f"Link is active for 15 minutes."
            )

            send_mail(
                subject='Welcome to YouTube! Email Verification',
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False
            )
        
        return HttpResponseRedirect(self.get_success_url())

    
class LoginUserView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.user

        login(self.request, user = user)

        return super().form_valid(form)

        
class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)
        except:
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            Channel.objects.create(
                user = user,
                title = user.username.title(),
                description = ''
            )

            return redirect('login')
        
        return redirect('register')


class HistoryView(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'history.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['videos'] = Video.objects.filter(video_watchs__user__id = self.request.user.id)

        return data


class VideoDetailView(DetailView):
    model = Video
    template_name = 'video.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['subcribed_channel'] = [chan.channel.id for chan in self.request.user.followed_channels.all()]
        data['liked_videos'] = [like.video.id for like in self.request.user.liked_videos.all()]

        is_watched = Watchs.objects.filter(user__id = self.request.user.id).filter(video__id = data['video'].id).exists()

        if not is_watched:
            Watchs.objects.create(
                user = self.request.user,
                video = data['video']
            )

        return data

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            comment = request.POST.get('comment', '')

            video = self.get_object()

            Comment.objects.create(
                user = request.user,
                video = video,
                comment = comment
            )

            return redirect('video_detail', pk = video.id)
            

class SubscribeView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        channel = Channel.objects.get(pk = pk)

        Following.objects.create(
            user = user,
            channel = channel
        )

        return redirect('channel_info', pk = channel.id)


class UnsubscribeView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        channel = Channel.objects.get(pk = pk)
        following = Following.objects.filter(user__id = user.id).get(channel__id = channel.id)

        following.delete()

        return redirect('channel_info', pk = channel.id)


class AddLikeView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        video = Video.objects.get(pk = pk)
        like = Like.objects.create(
            user = user,
            video = video
        )


        return redirect('video_detail', pk = pk)


class RemoveLikeView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        video = Video.objects.get(pk = pk)
        like = Like.objects.filter(user__id = user.id).get(video__id = video.id)

        like.delete()

        return redirect('video_detail', pk = pk)


class ShotsDetailView(DetailView):
    model = Video
    template_name = 'shorts.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['subcribed_channel'] = [chan.channel.id for chan in self.request.user.followed_channels.all()]
        data['liked_videos'] = [like.video.id for like in self.request.user.liked_videos.all()]

        is_watched = Watchs.objects.filter(user__id = self.request.user.id).filter(video__id = data['video'].id).exists()

        if not is_watched:
            Watchs.objects.create(
                user = self.request.user,
                video = data['video']
            )

        return data

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            comment = request.POST.get('comment', '')

            video = self.get_object()

            Comment.objects.create(
                user = request.user,
                video = video,
                comment = comment
            )

            return redirect('shorts_detail', pk = video.id)


class AddLikeShortsView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        video = Video.objects.get(pk = pk)
        
        Like.objects.create(
            user = user,
            video = video
        )


        return redirect('shorts_detail', pk = pk)


class RemoveLikeShortsView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        video = Video.objects.get(pk = pk)
        like = Like.objects.filter(user__id = user.id).get(video__id = video.id)

        like.delete()

        return redirect('shorts_detail', pk = pk)


class MyChannelView(LoginRequiredMixin, ListView):
    model = Video
    context_object_name = 'videos'
    template_name = 'my-channel.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['videos'] = Video.objects.filter(channel__id = self.request.user.channel.id)


class DeleteVideoView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        video = Video.objects.get(pk = pk)
        if video.channel.user.id == user.id:
            video.delete()

        return redirect('my_channel')


class AddVideoView(LoginRequiredMixin, CreateView):
    form_class = CreateVideoForm
    template_name = 'create-video.html'
    success_url = reverse_lazy('my_channel')

    def form_valid(self, form):
        video = form.save(commit=False)
        video.channel = self.request.user.channel
        video.save()
        followers_email = [follower.user.email for follower in self.request.user.channel.channel_followers.all()]
        print(followers_email)

        if followers_email:
            watch_url = self.request.build_absolute_uri(
                    reverse(
                        f'{'video_detail' if video.type == 'video' else 'shorts_detail'}',
                        kwargs = {
                            'pk': video.id
                        }
                    )
                )

            html_message = f"""
                <!DOCTYPE html>
                <html lang="ru">
                <head>
                  <meta charset="UTF-8">
                  <title>New video in channel!</title>
                </head>
                <body style="margin: 0; padding: 40px 15px; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
                  <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 540px; background-color: #ffffff; border-radius: 20px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); padding: 40px 36px;">
                    <tr>
                      <td>
                        <div style="font-size: 26px; font-weight: 800; color: #02B15F; margin-bottom: 24px; letter-spacing: -0.5px;">
                          YouTube
                        </div>
                        <h1 style="margin: 0 0 16px 0; font-size: 20px; font-weight: 700; color: #0f172a; line-height: 1.3;">
                            { self.request.user.channel.title } posted a new video!
                        </h1>
                        <p style="margin: 0 0 24px 0; font-size: 15px; color: #475569; line-height: 1.5;">
                          For watch the video click to link under the text:
                        </p>
                        <div style="border: 2px dashed #cbd5e1; border-radius: 14px; background-color: #ffffff; padding: 20px; text-align: center; margin-bottom: 24px;">
                          <a href="{watch_url}" target="_blank" style="display: inline-block; background-color: #02B15F; color: #ffffff; text-decoration: none; font-size: 16px; font-weight: 600; padding: 12px 32px; border-radius: 8px;">
                            Watch Video
                          </a>
                        </div>
                        <div style="text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #f1f5f9; padding-top: 20px;">
                          &copy; 2026 YouTube.
                        </div>
                      </td>
                    </tr>
                  </table>
                </body>
                </html>
            """

            plain_message = (
                f"{self.request.user.channel.title} posted a new video!\n\n"
                f"For watch video click to this link:\n{watch_url}\n\n"
            )

            send_mail(
                subject=f'{self.request.user.channel.title} posted a new video!',
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=followers_email,
                html_message=html_message,
                fail_silently=False
            )

        return super().form_valid(form)
  

class UpdateVideoView(LoginRequiredMixin, UpdateView):
    model = Video
    form_class = UpdateVideoForm
    template_name = 'update-video.html'
    success_url = reverse_lazy('my_channel')

    def get(self, request, *args, **kwargs):
        video = Video.objects.get(pk = kwargs.get('pk'))

        if video.channel.id != request.user.channel.id:
            return redirect('my_channel')

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Video.objects.filter(channel__id = self.request.user.channel.id)
    

    def form_valid(self, form):
        video = form.save(commit=False)
        video.channel = self.request.user.channel
        video.save()

        return super().form_valid(form)
    

class MyPlaylistsView(LoginRequiredMixin, ListView):
    model = Playlist
    context_object_name = 'playlists'
    template_name = 'my-playlists.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['playlists'] = Playlist.objects.filter(channel__id = self.request.user.channel.id)

        return data 


class DeletePlaylistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        playlist = Playlist.objects.get(pk = kwargs.get('pk'))
        if request.user.channel.id == playlist.channel.id:
            playlist.delete()

        return redirect('my_playlists')


class AddPlaylistView(LoginRequiredMixin, CreateView):
    form_class = CreatePlaylistForm
    template_name = 'create-playlist.html'
    success_url = reverse_lazy('my_playlists')

    def form_valid(self, form):
        playlist = form.save(commit=False)
        playlist.channel = self.request.user.channel
        playlist.save()

        return super().form_valid(form)


class UpdatPlaylistView(LoginRequiredMixin, UpdateView):
    model = Playlist
    form_class = CreatePlaylistForm
    template_name = 'update-playlist.html'
    success_url = reverse_lazy('my_playlists')

    def form_valid(self, form):
        playlist = form.save(commit=False)
        playlist.channel = self.request.user.channel
        playlist.save()

        return super().form_valid(form)


class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = 'playlist-info.html'
    context_object_name = 'playlist'


class RemoveVideoFromPlaylistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        playlist_video = PlaylistVideos.objects.get(pk = kwargs.get('pk'))
        playlist_id = playlist_video.playlist.id

        if request.user.channel.id == playlist_video.playlist.channel.id:
            playlist_video.delete()

        return redirect('playlist_info', pk = playlist_id)


class AddVideoToPlaylistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        video = Video.objects.get(pk = kwargs.get('video_id'))
        playlist = Playlist.objects.get(pk = kwargs.get('playlist_id'))
        is_exists = PlaylistVideos.objects.filter(video__id = video.id).filter(playlist__id = playlist.id).exists()

        if not is_exists:
            PlaylistVideos.objects.create(
                video = video,
                playlist = playlist
            )

        if video.type == 'video':
            return redirect('video_detail', pk = video.id)

        return redirect('shorts_detail', pk = video.id)


class ChannelDetailViews(DetailView):
    model = Channel
    context_object_name = 'channel'
    template_name = 'channel-info.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['subcribed_channel'] = [channel.channel.id for channel in self.request.user.followed_channels.all()]

        return data


class DeleteFromHistoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        history_video = Watchs.objects.filter(user__id = request.user.id).get(video__id = kwargs.get('pk'))

        if request.user.id == history_video.user.id:
            history_video.delete()

        return redirect('history')


class ChannelPlaylistDetailViews(DetailView):
    model = Channel
    context_object_name = 'channel'
    template_name = 'channel-playlist.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['subcribed_channel'] = [channel.channel.id for channel in self.request.user.followed_channels.all()]

        return data


class LogoutUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)

        return redirect('home')