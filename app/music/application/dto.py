from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.music.domain.roles import StatusMusic


class MediaSourceInDTO(BaseModel):
    original_url: str
    

class MediaSourceOutDTO(BaseModel):
    id: UUID
    title: Optional[str] = None
    original_url: str
    channel_name: Optional[str] = None
    duration_seconds: Optional[int] = None
    status: str | StatusMusic
    audio_file_path: Optional[str] = None
    created_at: datetime
    deleted_at: Optional[datetime] = None

    @classmethod
    def from_domain(cls, model):
        return MediaSourceOutDTO(
            id=model.id,
            title=model.title,
            original_url=model.original_url,
            channel_name=model.channel_name,
            duration_seconds=model.duration_seconds,
            status=model.status,
            audio_file_path=model.audio_file_path,
            created_at=model.created_at,
            deleted_at=model.deleted_at
        )
    

class MediaSourceUpdateInDTO(BaseModel):
    title: str
    original_url: str
    channel_name: str
    duration_seconds: int
    status: str | StatusMusic
    audio_file_path: str


class FinishDownloadMusicDTO(BaseModel):
    id: UUID
    title: Optional[str] = None
    channel_name: Optional[str] = None
    duration_seconds: Optional[int] = None
    audio_file_path: Optional[str] = None
