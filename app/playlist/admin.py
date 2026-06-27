from django.contrib import admin

from app.playlist.infrastructure.models import Playlist, PlaylistTrack, Track

# Register your models here.
admin.site.register(Playlist)
admin.site.register(PlaylistTrack)
admin.site.register(Track)
