from uuid import UUID

from app.playlist.domain.entities import PlaylistEntity
from app.playlist.domain.repositories import IPlaylistRepository
from app.playlist.infrastructure.models import Playlist


class PlaylistRepository(IPlaylistRepository):
    def save(self, playlist: PlaylistEntity) -> PlaylistEntity:
        Playlist.objects.update_or_create(
            id=playlist.id,
            defaults={
                'name': playlist.name,
                'user': playlist.user,
                'created_at': playlist.created_at,
                'deleted_at': playlist.deleted_at
            }
        )

        return playlist

    def find_by_id(self, id: UUID) -> PlaylistEntity | None:
        try:
            return self._to_model(Playlist.objects.get(id=id))

        except Playlist.DoesNotExist:
            return None    
        
    def find_by_name(self, name: str) -> PlaylistEntity | None:
        try:
            return self._to_model(Playlist.objects.get(name=name))

        except Playlist.DoesNotExist:
            return None    
        
    def verify_exists_playlist_by_name(self, name: str) -> bool:
        return Playlist.objects.filter(name=name).exists()

    def _to_model(self, model: Playlist) -> PlaylistEntity:
        return PlaylistEntity(
            id=model.id,
            name=model.name,
            user=model.user,
            created_at=model.created_at,
            deleted_at=model.deleted_at
        )
