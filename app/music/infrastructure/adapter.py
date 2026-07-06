from uuid import UUID

from app.music.domain.adapters import IDownloadMusicStartAdapter
from app.music.infrastructure.tasks import download_music


class DownloadMusicStartAdapter(IDownloadMusicStartAdapter):
    def download(self, id: UUID, url: str) -> None:
        download_music.delay(id, url)
