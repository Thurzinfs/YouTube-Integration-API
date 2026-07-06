from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema

from app.music.application.dto import MediaSourceInDTO, MediaSourceOutDTO
from app.music.domain.roles import StatusMusic


class MediaSourceIn(Schema):
    original_url: str

    def to_dto(self) -> MediaSourceInDTO:
        return MediaSourceInDTO(
            original_url=self.original_url
        )
    

class MediaSourceOut(Schema):
    id: UUID
    title: Optional[str] = None
    original_url: str
    channel_name: Optional[str] = None
    duration_seconds: Optional[int] = None
    status: str | StatusMusic
    audio_file_path: Optional[str] = None
    created_at: datetime
    deleted_at: Optional[datetime] = None

    @staticmethod
    def from_domain(dto: MediaSourceOutDTO):
        return MediaSourceOut(
            id=dto.id,
            title=dto.title,
            original_url=dto.original_url,
            channel_name=dto.channel_name,
            duration_seconds=dto.duration_seconds,
            status=dto.status,
            audio_file_path=dto.audio_file_path,
            created_at=dto.created_at,
            deleted_at=dto.deleted_at
        )
    

class MediaSourcceUpdateIn(Schema):
    title: str
    original_url: str
    channel_name: str
    duration_seconds: int
    status: str | StatusMusic
    audio_file_path: str
