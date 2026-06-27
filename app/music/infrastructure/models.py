from uuid import uuid4

from django.db import models

from app.music.domain.roles import StatusMusic


class MediaSource(models.Model):
    """
    Modelo do banco de dados referente as musicas registradas
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    original_url = models.URLField()
    title = models.CharField(max_length=255)
    channel_name = models.CharField(max_length=255)
    duration_seconds = models.IntegerField()
    status = models.CharField(
        max_length=40, choices=StatusMusic, default=StatusMusic.pending
    )
    audio_file_path = models.FileField(upload_to='music/audio/', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'media_source'
