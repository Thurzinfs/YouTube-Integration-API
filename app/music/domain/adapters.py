from abc import ABC
from uuid import UUID


class IDownloadMusicStartAdapter(ABC):
    def download(self, id: UUID, url: str) -> None:
        ...
