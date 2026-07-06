from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.music.domain.exceptions import ConflictMediaSourceFieldException, FieldMediaSourceRequiredException
from app.music.domain.roles import StatusMusic


@dataclass
class MediaSourceEntity:
    id: UUID = field(default_factory=uuid4)
    original_url: str = field(default='')
    title: str | None = field(default=None)
    channel_name: str | None = field(default=None)
    duration_seconds: int  = field(default=0)
    status: StatusMusic | str = field(default=StatusMusic.pending)
    audio_file_path: str | None = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: datetime | None = field(default=None)

    def deactive(self) -> None:
        if self.deactive is False:
            raise ConflictMediaSourceFieldException('media source already deactivate')

        self.deleted_at = datetime.now()

    def change_status(self, new_status: StatusMusic) -> None:
        if not new_status:
            raise FieldMediaSourceRequiredException('field status is required')

        self.status = new_status

    def change_audio_path(self, path: str) -> None:
        if not path:
            raise FieldMediaSourceRequiredException('field path is required')

        self.audio_file_path = path

    def change_channel_name(self, channel_name: str) -> None:
        if not channel_name:
            raise FieldMediaSourceRequiredException('field channel name is required')

        self.channel_name = channel_name

    def change_duration(self, seg: int) -> None:
        if not seg:
            raise FieldMediaSourceRequiredException('field segunds is required')

        self.duration_seconds = seg

    def change_title(self, new_title: str) -> None:
        if not new_title:
            raise FieldMediaSourceRequiredException('field title is required')

        self.title = new_title
