from abc import ABC, abstractmethod
from uuid import UUID

from app.music.domain.entities import MediaSourceEntity


class IMediaSourceRepository(ABC):
    @abstractmethod
    def save(self, user: MediaSourceEntity) -> MediaSourceEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> MediaSourceEntity | None:
        ...

    @abstractmethod
    def find_by_channel_name(self, email: str) -> MediaSourceEntity | None:
        ...

    @abstractmethod
    def verify_exists_title(self, email: str) -> bool:
        ...

    @abstractmethod
    def verify_exists_url(self, url: str) -> bool:
        ...
