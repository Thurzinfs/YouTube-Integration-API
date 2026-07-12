from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.playlist.domain.exceptions import ConflictFieldException, FieldRequiredPlaylistException


@dataclass
class PlaylistEntity:
    id: UUID = field(default_factory=uuid4)
    name: str = field(default='')
    user: UUID | None = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: datetime | None = field(default=None)

    def deactive(self):
        if self.deleted_at is not None:
            raise ConflictFieldException('playlist already deleted')
        
        self.deleted_at = datetime.now()

    def change_name(self, new_name: str):
        if not new_name:
            raise FieldRequiredPlaylistException('field name is required')

        self.name = new_name
    

@dataclass
class TrackEntity:
    id: UUID = field(default_factory=uuid4)
    user: UUID | None = field(default=None)
    media_source: UUID | None = field(default=None)
    custom_title: str = field(default='')
    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: datetime | None = field(default=None)

    def deactive(self):
        if self.deleted_at is not None:
            ...

        self.deleted_at = datetime.now()

    def change_custom_title(self, new_title: str):
        if not new_title:
            ...

        self.custom_title = new_title
