from dependency_injector import containers, providers

from app.music.application.use_case import DeactiveMusicUseCase, FinishDownlaodMusicUseCase, ResponseMusicUseCase, SearchMusicsBySimilarityUseCase, StartRegisterMusicUseCase
from app.music.infrastructure.adapter import DownloadMusicStartAdapter
from app.music.infrastructure.repository import MediaSourceRepository


class MusicContainer(containers.DeclarativeContainer):
    music_repo = providers.Factory(MediaSourceRepository)

    music_adapter = providers.Factory(DownloadMusicStartAdapter)


    start_register_music_use_case = providers.Factory(
        StartRegisterMusicUseCase,
        music_repo=music_repo,
        music_adapter=music_adapter
    )

    finish_download_music_use_case = providers.Factory(
        FinishDownlaodMusicUseCase,
        music_repo=music_repo
    )
    
    response_music_use_case = providers.Factory(
        ResponseMusicUseCase,
        music_repo=music_repo
    )

    search_musics_by_similarity_use_case = providers.Factory(
        SearchMusicsBySimilarityUseCase,
        music_repo=music_repo
    )

    deactive_music_use_case = providers.Factory(
        DeactiveMusicUseCase,
        music_repo=music_repo
    )
    