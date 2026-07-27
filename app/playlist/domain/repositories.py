from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.playlist.domain.entities import PlaylistEntity, PlaylistTrackEntity, TrackEntity


class IPlaylistRepository(ABC):
    @abstractmethod
    def save(self, playlist: PlaylistEntity) -> PlaylistEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> PlaylistEntity | None:
        ...

    @abstractmethod
    def find_by_name(self, name: str) -> PlaylistEntity | None:
        ...

    @abstractmethod
    def list_playlist_by_user(self, id: UUID) -> List[PlaylistEntity]:
        ...

    @abstractmethod
    def verify_exists_playlist_by_name(self, name: str) -> bool:
        ...

    @abstractmethod
    def delete_by_id(self, id: UUID) -> None:
        ...


class ITrackRepository(ABC):
    @abstractmethod
    def save(self, track: TrackEntity) -> TrackEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> TrackEntity | None:
        ...

    @abstractmethod
    def find_many_by_ids(self, ids: List[UUID]) -> List[TrackEntity]:
        ...

    @abstractmethod
    def find_by_custom_title(self, custom_title: str) -> TrackEntity | None:
        ...

    @abstractmethod
    def list_track_by_user(self, user: UUID) -> List[TrackEntity]:
        ...

    @abstractmethod
    def delete_by_id(self, id: UUID) -> None:
        ...

    @abstractmethod
    def verify_exists_track_by_custom_title(self, custom_title: str) -> bool:
        ...


class IPlaylistTrackRepository(ABC):
    @abstractmethod
    def save(self, entity: PlaylistTrackEntity) -> PlaylistTrackEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> PlaylistTrackEntity | None:
        ...

    @abstractmethod
    def find_by_position(self, position: int) -> PlaylistTrackEntity | None:
        ...

    @abstractmethod
    def count_all_playlist_track(self, id: UUID) -> int:
        ...

    @abstractmethod
    def verify_exists_playlist_track_by_playlist_track(self, track: UUID, playlist: UUID) -> bool:
        ...
    
    @abstractmethod
    def verify_exists_position(self, position: int) -> bool:
        ...

    @abstractmethod
    def delete_by_id(self, id: UUID) -> None:
        ...

    @abstractmethod
    def list_playlist_track_by_playlist(self, playlist: UUID) -> List[PlaylistTrackEntity]:
        ...
    