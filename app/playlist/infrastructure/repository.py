from typing import List
from uuid import UUID

from passlib import exc

from app.playlist.domain.entities import PlaylistEntity, PlaylistTrackEntity, TrackEntity
from app.playlist.domain.repositories import IPlaylistRepository, IPlaylistTrackRepository, ITrackRepository
from app.playlist.infrastructure.models import Playlist, PlaylistTrack, Track


class PlaylistRepository(IPlaylistRepository):
    def save(self, playlist: PlaylistEntity) -> PlaylistEntity:
        Playlist.objects.update_or_create(
            id=playlist.id,
            defaults={
                'name': playlist.name,
                'user_id': playlist.user,
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

    def list_playlist_by_user(self, id: UUID) -> List[PlaylistEntity]:
        try:
            return [
                self._to_model(playlist)
                for playlist in Playlist.objects.filter(user=id).all()
            ]

        except Playlist.DoesNotExist:
            return []

    def delete_by_id(self, id: UUID) -> None:
        Playlist.objects.filter(id=id).delete()

    def _to_model(self, model: Playlist) -> PlaylistEntity:
        return PlaylistEntity(
            id=model.id,
            name=model.name,
            user=model.user.id,
            created_at=model.created_at,
            deleted_at=model.deleted_at
        )


class TrackRepository(ITrackRepository):
    def save(self, track: TrackEntity) -> TrackEntity:
        Track.objects.update_or_create(
            id=track.id,
            defaults={
                'user_id': track.user,
                'media_source_id': track.media_source,
                'custom_title': track.custom_title,
                'added_at': track.added_at,
                'deleted_at': track.deleted_at
            }
        )

        return track
    
    def find_by_id(self, id: UUID) -> TrackEntity | None:
        try:
            return self._to_model(Track.objects.get(id=id))

        except Track.DoesNotExist:
            return None

    def find_many_by_ids(self, ids: List[UUID]) -> List[TrackEntity]:
        return [
            self._to_model(track)
            for track in Track.objects.filter(id__in=ids)
        ]
        
    def find_by_custom_title(self, custom_title: str) -> TrackEntity | None:
        try:
            return self._to_model(Track.objects.get(custom_title=custom_title))

        except Track.DoesNotExist:
            return None
        
    def verify_exists_track_by_custom_title(self, custom_title: str) -> bool:
        return Track.objects.filter(custom_title=custom_title).exists()

    def list_track_by_user(self, user: UUID) -> List[TrackEntity]:
        try:
            return [
                self._to_model(track)
                for track in Track.objects.filter(user=user).all()
            ]

        except Track.DoesNotExist:
            return []

    def delete_by_id(self, id: UUID) -> None:
        Track.objects.filter(id=id).delete()
    
    def _to_model(self, model: Track) -> TrackEntity:
        return TrackEntity(
            id=model.id,
            user=model.user.id,
            media_source=model.media_source.id,
            custom_title=model.custom_title,
            added_at=model.added_at,
            deleted_at=model.deleted_at
        )


class PlaylistTrackRepository(IPlaylistTrackRepository):
    def save(self, entity: PlaylistTrackEntity) -> PlaylistTrackEntity:
        PlaylistTrack.objects.update_or_create(
            id=entity.id,
            defaults={
                'playlist_id': entity.playlist,
                'track_id': entity.track,
                'position': entity.position,
                'deleted_at': entity.deleted_at
            }
        )

        return entity
    
    def find_by_id(self, id: UUID) -> PlaylistTrackEntity | None:
        try:
            return self._to_model(PlaylistTrack.objects.get(id=id))

        except PlaylistTrack.DoesNotExist:
            return None
        
    def find_by_position(self, position: int) -> PlaylistTrackEntity | None:
        try:
            return self._to_model(PlaylistTrack.objects.get(position=position))

        except PlaylistTrack.DoesNotExist:
            return None

    def count_all_playlist_track(self, id: UUID) -> int:
        return PlaylistTrack.objects.filter(playlist__id=id).count()

    def verify_exists_playlist_track_by_playlist_track(self, track: UUID, playlist: UUID) -> bool:
        return PlaylistTrack.objects.filter(playlist__id=playlist, track__id=track).exists()
        
    def verify_exists_position(self, position: int) -> bool:
        return PlaylistTrack.objects.filter(position=position).exists()

    def list_playlist_track_by_playlist(self, playlist: UUID) -> List[PlaylistTrackEntity]:
        try:
            return [
                self._to_model(playlist_track)
                for playlist_track in PlaylistTrack.objects.filter(playlist__id=playlist).order_by('position').all()
            ]

        except PlaylistTrack.DoesNotExist:
            return []

    def delete_by_id(self, id: UUID) -> None:
        PlaylistTrack.objects.filter(id=id).delete()
    
    def _to_model(self, model: PlaylistTrack) -> PlaylistTrackEntity:
        return PlaylistTrackEntity(
            id=model.id, 
            playlist=model.playlist.id,
            track=model.track.id,
            position=model.position,
            deleted_at=model.deleted_at
        )
