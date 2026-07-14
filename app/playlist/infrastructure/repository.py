from uuid import UUID

from app.playlist.domain.entities import PlaylistEntity, TrackEntity
from app.playlist.domain.repositories import IPlaylistRepository, ITrackRepository
from app.playlist.infrastructure.models import Playlist, Track


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


class TrackRepository(ITrackRepository):
    def save(self, track: TrackEntity) -> TrackEntity:
        Track.objects.update_or_create(
            id=track.id,
            defaults={
                'user': track.user,
                'media_source': track.media_source,
                'custom_title': track.custom_title,
                'added_at': track.added_at,
                'deleted_at': track.deleted_at
            }
        )

        return track
    
    def find_by_id(self, id: UUID) -> TrackEntity | None:
        try:
            self._to_model(Track.objects.get(id=id))

        except Track.DoesNotExist:
            return None
        
    def find_by_custom_title(self, custom_title: str) -> TrackEntity | None:
        try:
            self._to_model(Track.objects.get(custom_title=custom_title))

        except Track.DoesNotExist:
            return None
        
    def verify_exists_track_by_custom_title(self, custom_title: str) -> bool:
        return Track.objects.filter(custom_title=custom_title).exists()
    
    def _to_model(self, model: Track) -> TrackEntity:
        return TrackEntity(
            id=model.id,
            user=model.user,
            media_source=model.media_source,
            custom_title=model.custom_title,
            added_at=model.added_at,
            deleted_at=model.deleted_at
        )
