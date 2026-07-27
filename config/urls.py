from django.contrib import admin
from django.urls import path

from ninja import NinjaAPI

from app.accounts.api.views import router as account_router
from app.music.api.views import router as music_router
from app.playlist.api.views import router_playlist, track_router, playlist_track_router

api = NinjaAPI(title='Music YouTube API', docs_url='/docs/')


@api.get('/health', tags=['Health'])
def health_check(request):
    return {'msg': 'OK'}


api.add_router('/account', account_router, tags=['Accounts'])
api.add_router('/music', music_router, tags=['Music'])
api.add_router('/playlist', router_playlist, tags=['Playlist'])
api.add_router('/track', track_router, tags=['Track'])
api.add_router('/playlist/track', playlist_track_router, tags=['Playlist Track'])

urlpatterns = [path('admin/', admin.site.urls), path('api/v1/', api.urls)]
