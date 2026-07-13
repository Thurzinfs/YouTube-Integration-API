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


class PlaylistUpdateDTO(BaseModel):
    name: Optional[str] = None


class TrackInDTO(BaseModel):
    user: Optional[UUID] = None
    media_source: Optional[UUID] = None
    custom_title: str


class TrackOutDTO(BaseModel):
    id: UUID
    user: Optional[UUID] = None
    media_source: Optional[UUID] = None
    custom_title: str
    created_at: datetime
    deleted_at: Optional[datetime] = None


class TrackUpdateDTO(BaseModel):
    custom_title: Optional[str] = None
