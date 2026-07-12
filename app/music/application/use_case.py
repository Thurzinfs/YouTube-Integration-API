from typing import List
from uuid import UUID

from app.accounts.domain.exceptions import ConflictFieldException
from app.music.application.dto import FinishDownloadMusicDTO, MediaSourceInDTO, MediaSourceOutDTO
from app.music.domain.adapters import IDownloadMusicStartAdapter
from app.music.domain.entities import MediaSourceEntity
from app.music.domain.exceptions import NotFoundMediaSourceException
from app.music.domain.repositories import IMediaSourceRepository
from app.music.domain.roles import StatusMusic


class StartRegisterMusicUseCase:
    def __init__(self, music_repo: IMediaSourceRepository, music_adapter: IDownloadMusicStartAdapter) -> None:
        self.music_repo = music_repo
        self.music_adapter = music_adapter

    def execute(self, dto: MediaSourceInDTO) -> MediaSourceOutDTO:
        if self.music_repo.verify_exists_url(dto.original_url):
            raise ConflictFieldException('music url is already exists')
        
        music = MediaSourceEntity(
            original_url=dto.original_url,
            status=StatusMusic.processing
        )

        self.music_repo.save(music)

        self.music_adapter.download(music.id, music.original_url)

        return MediaSourceOutDTO.from_domain(music)


class FinishDownlaodMusicUseCase:
    def __init__(self, music_repo: IMediaSourceRepository) -> None:
        self.music_repo = music_repo

    def execute(self, dto: FinishDownloadMusicDTO):
        music = self.music_repo.find_by_id(dto.id)
        print(music)
        if not music:
            raise NotFoundMediaSourceException('music not found')
        
        if dto.title is not None:
            music.change_title(dto.title)

        if dto.channel_name is not None:
            music.change_channel_name(dto.channel_name)

        if dto.duration_seconds is not None:
            music.change_duration(dto.duration_seconds)
        
        if dto.audio_file_path is not None:
            music.change_audio_path(dto.audio_file_path)
        
        music.change_status(StatusMusic.ready)

        self.music_repo.save(music)


class ResponseMusicUseCase:
    def __init__(self, music_repo: IMediaSourceRepository) -> None:
        self.music_repo = music_repo
    
    def execute(self, id: UUID) -> MediaSourceOutDTO:
        music = self.music_repo.find_by_id(id)
        if not music:
            raise NotFoundMediaSourceException('music not found')
        
        return MediaSourceOutDTO.from_domain(music)


class ListMusicsActivesUseCase:
    def __init__(self, music_repo: IMediaSourceRepository) -> None:
        self.music_repo = music_repo

    def execute(self) -> List[MediaSourceOutDTO]:
        musics = self.music_repo.list_all_musics()
        if not musics:
            return []
        
        return [
            MediaSourceOutDTO.from_domain(music)
            for music in musics
        ]


class SearchMusicsBySimilarityUseCase:
    def __init__(self, music_repo: IMediaSourceRepository) -> None:
        self.music_repo = music_repo

    def execute(self, term: str) -> List[MediaSourceOutDTO]:
        query = self.music_repo.search_by_similarity(term, 0.2)
        if not query:
            return []
        
        return [
            MediaSourceOutDTO.from_domain(model)
            for model in query
        ]


class DeactiveMusicUseCase:
    def __init__(self, music_repo: IMediaSourceRepository) -> None:
        self.music_repo = music_repo

    def execute(self, id: UUID) -> MediaSourceOutDTO:
        music = self.music_repo.find_by_id(id)
        if not music:
            raise NotFoundMediaSourceException('music not found')
        
        music.deactive()

        self.music_repo.save(music)

        return MediaSourceOutDTO.from_domain(music)
