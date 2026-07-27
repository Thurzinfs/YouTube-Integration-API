from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema

from app.playlist.application.dto import PlaylistInDTO, PlaylistOutDTO, PlaylistTrackInDTO, PlaylistTrackOutDTO, PlaylistTrackUpdateDTO, PlaylistUpdateDTO, TrackInDTO, TrackOutDTO


class PlaylistIn(Schema):
    name: str
    user: UUID

    def to_dto(self) -> PlaylistInDTO:
        return PlaylistInDTO(
            name=self.name,
            user=self.user
        )


class PlaylistOut(Schema):
    id: UUID
    name: str
    user: UUID
    created_at: datetime
    deleted_at: Optional[datetime] = None

    @staticmethod
    def from_domain(dto: PlaylistOutDTO):
        return PlaylistOut(
            id=dto.id,
            name=dto.name,
            user=dto.user,
            created_at=dto.created_at,
            deleted_at=dto.deleted_at
        )


class UpdatePlaylistIn(Schema):
    name: Optional[str] = None

    def to_dto(self) -> PlaylistUpdateDTO:
        return PlaylistUpdateDTO(
            name=self.name
        )


class TrackIn(Schema):
    user: UUID
    media_source: UUID
    custom_title: str

    def to_dto(self) -> TrackInDTO:
        return TrackInDTO(
            user=self.user,
            media_source=self.media_source,
            custom_title=self.custom_title
        )


class TrackOut(Schema):
    id: UUID
    user: Optional[UUID] = None
    media_source: Optional[UUID] = None
    custom_title: str
    created_at: datetime
    deleted_at: Optional[datetime] = None

    @staticmethod
    def from_domain(dto: TrackOutDTO):
        return TrackOut(
            id=dto.id,
            user=dto.user,
            media_source=dto.media_source,
            custom_title=dto.custom_title,
            created_at=dto.created_at,
            deleted_at=dto.deleted_at
        )


class TrackUpdate(Schema):
    custom_title: Optional[str] = None


class PlaylistTrackIn(Schema):
    playlist: UUID
    track: UUID
    position: int

    def to_dto(self) -> PlaylistTrackInDTO:
        return PlaylistTrackInDTO(
            playlist=self.playlist,
            track=self.track,
            position=self.position
        )


class PlaylistTrackOut(Schema):
    id: UUID
    playlist: UUID
    track: UUID
    position: int
    deleted_at: datetime

    @staticmethod
    def from_domain(dto: PlaylistTrackOutDTO):
        return PlaylistTrackOut(
            id=dto.id,
            playlist=dto.playlist, 
            track=dto.track,
            position=dto.position,
            deleted_at=dto.deleted_at
        )


class PlaylistTrackUpdate(Schema):
    position: int

    def to_dto(self) -> PlaylistTrackUpdateDTO:
        return PlaylistTrackUpdateDTO(
            position=self.position
        )
