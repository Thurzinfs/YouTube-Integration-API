from abc import ABC, abstractmethod
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
    def verify_exists_playlist_by_name(self, name: str) -> bool:
        ...


class ITrackRepository(ABC):
    @abstractmethod
    def save(self, track: TrackEntity) -> TrackEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> TrackEntity | None:
        ...

    @abstractmethod
    def find_by_custom_title(self, custom_title: str) -> TrackEntity | None:
        ...

    @abstractmethod
    def verify_exists_track_by_custom_title(self, custom_title: str) -> TrackEntity | None:
        ...
