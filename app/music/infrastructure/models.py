from uuid import uuid4

from django.db import models

from app.music.domain.roles import StatusMusic

from django.contrib.postgres.indexes import GinIndex


class MediaSource(models.Model):
    """
    Modelo do banco de dados referente as musicas registradas
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    original_url = models.URLField()
    title = models.CharField(max_length=255, null=True)
    channel_name = models.CharField(max_length=255, null=True)
    duration_seconds = models.IntegerField()
    status = models.CharField(
        max_length=40, choices=StatusMusic, default=StatusMusic.pending
    )
    audio_file_path = models.FileField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        indexes = [
            GinIndex(fields=['title'], name='music_name_trgm', opclasses=['gin_trgm_ops']),
            GinIndex(fields=['channel_name'], name='music_channel_trgm', opclasses=['gin_trgm_ops'])
        ]

        db_table = 'media_source'
