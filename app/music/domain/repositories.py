from abc import ABC, abstractmethod
from uuid import UUID

from typing import List

from app.music.domain.entities import MediaSourceEntity


class IMediaSourceRepository(ABC):
    @abstractmethod
    def save(self, music: MediaSourceEntity) -> MediaSourceEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> MediaSourceEntity | None:
        ...

    @abstractmethod
    def find_by_channel_name(self, channel_name: str) -> MediaSourceEntity | None:
        ...

    @abstractmethod
    def list_all_musics(self) -> List[MediaSourceEntity]:
        ...

    @abstractmethod
    def search_by_similarity(self, term: str, conf: float, limit: int = 20) -> List[MediaSourceEntity]:
        ...

    @abstractmethod
    def verify_exists_title(self, title: str) -> bool:
        ...

    @abstractmethod
    def verify_exists_url(self, original_url: str) -> bool:
        ...
