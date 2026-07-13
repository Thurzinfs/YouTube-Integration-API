from uuid import uuid4

from django.db import models


class Playlist(models.Model):
    """
    Coleçao das musicas dos usuarios
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=120, null=False)
    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'playlists'


class Track(models.Model):
    """
    Ligacao entre a musica e o usuario
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    media_source = models.ForeignKey(
        'music.MediaSource', on_delete=models.CASCADE
    )
    custom_title = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'tracks'


class PlaylistTrack(models.Model):
    """
    Relaciona a playlist as musicas(Tracks) presentes para o usuario
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    playlist = models.ForeignKey(
        'Playlist', on_delete=models.CASCADE, null=False
    )
    track = models.ForeignKey('Track', on_delete=models.CASCADE, null=False)
    position = models.IntegerField()
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'playlists_track'
