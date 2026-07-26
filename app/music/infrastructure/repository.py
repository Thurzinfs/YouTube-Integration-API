from typing import List
from uuid import UUID

from app.music.domain.entities import MediaSourceEntity
from app.music.domain.repositories import IMediaSourceRepository
from app.music.domain.roles import StatusMusic
from app.music.infrastructure.models import MediaSource

from django.db.models.functions import Greatest

from django.contrib.postgres.search import TrigramSimilarity


class MediaSourceRepository(IMediaSourceRepository):
    def save(self, music: MediaSourceEntity) -> MediaSourceEntity:
        MediaSource.objects.update_or_create(
            id=music.id,
            defaults={
                'original_url': music.original_url,
                'title': music.title,
                'channel_name': music.channel_name,
                'duration_seconds': music.duration_seconds,
                'status': music.status,
                'audio_file_path': music.audio_file_path,
                'created_at': music.created_at,
                'deleted_at': music.deleted_at
            }
        )
        
        return music
    
    def find_by_id(self, id: UUID) -> MediaSourceEntity | None:
        try:
            return self._to_entity(MediaSource.objects.get(id=id))

        except MediaSource.DoesNotExist:
            return None

    def find_many_by_ids(self, ids: List[MediaSourceEntity]) -> List[MediaSourceEntity]:
        return [
            self._to_entity(music)
            for music in MediaSource.objects.filter(id__in=ids)
        ]
        
    def find_by_channel_name(self, channel_name: str) -> MediaSourceEntity | None:
        try:
            return self._to_entity(MediaSource.objects.get(channel_name=channel_name))

        except MediaSource.DoesNotExist:
            return None
        
    def list_all_musics(self) -> List[MediaSourceEntity]:
        return [
            self._to_entity(model)
            for model in MediaSource.objects.filter(status=StatusMusic.ready, deleted_at__isnull=True).all()
        ]
        
    def search_by_similarity(self, term: str, conf: float, limit: int = 20) -> List[MediaSourceEntity]:
        query_set = MediaSource.objects.filter(deleted_at__isnull=True, status=StatusMusic.ready).annotate(sim=Greatest(
            TrigramSimilarity('title', term),
            TrigramSimilarity('channel_name', term)
        )).filter(sim__gt=conf).order_by('-sim')[:limit]

        return [
            self._to_entity(model)
            for model in query_set
        ]
        
    def verify_exists_title(self, title: str) -> bool:
        return MediaSource.objects.filter(title=title).exists()

    def verify_exists_url(self, original_url: str) -> bool:
        return MediaSource.objects.filter(original_url=original_url).exists()
    
    def _to_entity(self, model: MediaSource) -> MediaSourceEntity:
        return MediaSourceEntity(
            id=model.id,
            title=model.title,
            original_url=model.original_url,
            channel_name=model.channel_name,
            duration_seconds=model.duration_seconds,
            status=model.status,
            audio_file_path=model.audio_file_path.url if model.audio_file_path else None,
        )
