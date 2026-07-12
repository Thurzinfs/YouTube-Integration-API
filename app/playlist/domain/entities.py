from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class PlaylistEntity:
    id: UUID = field(default_factory=uuid4)
    name: str = field(default='')
    user: UUID | None = field(default=None)
