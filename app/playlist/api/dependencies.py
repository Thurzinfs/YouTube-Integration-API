from dependency_injector import containers, providers

from app.accounts.infrastructure.repository import UserRepository
from app.music.infrastructure.repository import MediaSourceRepository
from app.playlist.application.use_case import ListMusicsInPlaylistTrack, ListPlaylistByUserUseCase, ListTrackByUserUseCase, PlaylistUpdateUseCase, RegisterPlaylistTrackUseCase, RegisterPlaylistUseCase, RegisterTrackUseCase, RemoveMusicInPlaylistUseCase, RemoveMusicInTrackUseCase, RemovePlaylistUseCase, ResponsePlaylistUseCase
from app.playlist.infrastructure.repository import PlaylistRepository, PlaylistTrackRepository, TrackRepository


class PlaylistModuleContainer(containers.DeclarativeContainer):
    playlist_repo = providers.Factory(PlaylistRepository)

    track_repo = providers.Factory(TrackRepository)

    playlist_track_repo = providers.Factory(PlaylistTrackRepository)

    user_repo = providers.Factory(UserRepository)

    media_source_repo = providers.Factory(MediaSourceRepository)

    register_playlist_use_case = providers.Factory(
        RegisterPlaylistUseCase,
        playlist_repo=playlist_repo,
        user_repo=user_repo
    )

    list_playlist_by_user_use_case = providers.Factory(
        ListPlaylistByUserUseCase,
        playlist_repo=playlist_repo,
    )

    response_playlist_use_case = providers.Factory(
        ResponsePlaylistUseCase,
        playlist_repo=playlist_repo,
    )

    playlist_update_use_case = providers.Factory(
        PlaylistUpdateUseCase,
        playlist_repo=playlist_repo,
    )

    register_track_use_case = providers.Factory(
        RegisterTrackUseCase,
        track_repo=track_repo,
        user_repo=user_repo,
        media_source_repo=media_source_repo
    )

    list_track_use_case = providers.Factory(
        ListTrackByUserUseCase,
        track_repo=track_repo
    )

    register_playlist_track_use_case = providers.Factory(  
        RegisterPlaylistTrackUseCase,
        playlist_track_repo=playlist_track_repo,
        playlist_repo=playlist_repo,
        track_repo=track_repo,
        user_repo=user_repo
    )

    list_musics_in_playlist_use_case = providers.Factory(
        ListMusicsInPlaylistTrack,
        playlist_track_repo=playlist_track_repo,
        track_repo=track_repo,
        music_repo=media_source_repo
    )

    remove_music_in_playlist_use_case = providers.Factory(
        RemoveMusicInPlaylistUseCase,
        playlist_track_repo=playlist_track_repo,
        track_repo=track_repo
    )

    remove_music_in_track_use_case = providers.Factory(
        RemoveMusicInTrackUseCase,
        track_repo=track_repo
    )

    remove_playlist_use_case = providers.Factory(
        RemovePlaylistUseCase,
        playlist_repo=playlist_repo
    )
