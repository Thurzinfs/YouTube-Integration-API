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
