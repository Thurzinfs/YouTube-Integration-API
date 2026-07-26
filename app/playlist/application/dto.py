from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PlaylistInDTO(BaseModel):
    name: str
    user: UUID


class PlaylistOutDTO(BaseModel):
    id: UUID
    name: str
    user: UUID
    created_at: datetime
    deleted_at: Optional[datetime] = None

    @classmethod
    def from_domain(cls, model):
        return cls(
            id=model.id,
            name=model.name,
            user=model.user,
            created_at=model.created_at,
            deleted_at=model.deleted_at
        )


class PlaylistUpdateDTO(BaseModel):
    name: Optional[str] = None


class TrackInDTO(BaseModel):
    user: UUID
    media_source: UUID
    custom_title: str


class TrackOutDTO(BaseModel):
    id: UUID
    user: Optional[UUID] = None
    media_source: Optional[UUID] = None
    custom_title: str
    created_at: datetime
    deleted_at: Optional[datetime] = None

    @classmethod
    def from_domain(cls, model):
        return cls(
            id=model.id,
            user=model.user,
            media_source=model.media_source,
            custom_title=model.custom_title,
            created_at=model.created_at,
            deleted_at=model.deleted_at
        )


class TrackUpdateDTO(BaseModel):
    custom_title: Optional[str] = None


class PlaylistTrackInDTO(BaseModel):
    playlist: UUID
    track: UUID
    position: int


class PlaylistTrackOutDTO(BaseModel):
    id: UUID
    playlist: UUID
    track: UUID
    position: int
    deleted_at: datetime

    @classmethod
    def from_domain(cls, model):
        return cls(
            id=model.id,
            playlist=model.playlist, 
            track=model.track,
            position=model.position,
            deleted_at=model.deleted_at
        )


class PlaylistTrackUpdateDTO(BaseModel):
    position: int


class DeletePlaylistTrackInDTO(BaseModel):
    playlist_track: UUID
