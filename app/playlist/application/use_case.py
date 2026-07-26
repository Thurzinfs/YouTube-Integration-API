from uuid import UUID

from app.accounts.domain.exceptions import UserNotFoundException
from app.accounts.domain.repositories import IUserRepository
from app.music.domain.exceptions import FailedDownloadMusicException, NotFoundMediaSourceException
from app.music.domain.repositories import IMediaSourceRepository
from app.music.domain.roles import StatusMusic
from app.playlist.application.dto import PlaylistInDTO, PlaylistOutDTO, PlaylistUpdateDTO, TrackInDTO, TrackOutDTO
from app.playlist.domain.entities import PlaylistEntity, TrackEntity
from app.playlist.domain.exceptions import ConflictFieldException, PlaylistIsDeletedException, PlaylistNotFoundException
from app.playlist.domain.repositories import IPlaylistRepository, ITrackRepository


class RegisterPlaylistUseCase:
    def __init__(self, playlist_repo: IPlaylistRepository, user_repo: IUserRepository) -> None:
        self.playlist_repo = playlist_repo
        self.user_repo = user_repo

    def execute(self, dto: PlaylistInDTO):
        user =  self.user_repo.find_by_id(dto.user)
        if not user:
            raise UserNotFoundException('user not found')

        if self.playlist_repo.verify_exists_playlist_by_name(dto.name):
            raise ConflictFieldException('playlist name already exists')

        playlist = PlaylistEntity(
            name=dto.name,
            user=dto.user
        )

        self.playlist_repo.save(playlist)
        return PlaylistOutDTO.from_domain(playlist)


class ListPlaylistByUserUseCase:
    def __init__(self, playlist_repo: IPlaylistRepository) -> None:
        self.playlist_repo = playlist_repo

    def execute(self, user: UUID):
        playlists = self.playlist_repo.list_playlist_by_user(user)
        if not playlists:
            return []

        return [
            PlaylistOutDTO.from_domain(playlist)
            for playlist in playlists
        ]


class ResponsePlaylistUseCase:
    def __init__(self, playlist_repo: IPlaylistRepository) -> None:
        self.playlist_repo = playlist_repo

    def execute(self, id: UUID):
        playlist = self.playlist_repo.find_by_id(id)
        if not playlist:
            raise PlaylistNotFoundException('playlist not found')

        return PlaylistOutDTO.from_domain(playlist)


class PlaylistUpdateUseCase:
    def __init__(self, playlist_repo: IPlaylistRepository) -> None:
        self.playlist_repo = playlist_repo

    def execute(self, id: UUID, dto: PlaylistUpdateDTO):
        playlist = self.playlist_repo.find_by_id(id)
        if not playlist:
            raise PlaylistNotFoundException('playlist not found')

        if playlist.deleted_at is not None:
            raise PlaylistIsDeletedException('playlist is deleted')

        if dto.name:
            playlist.change_name(dto.name)

        self.playlist_repo.save(playlist)
        return PlaylistOutDTO.from_domain(playlist)


class RegisterTrackUseCase:
    def __init__(self, track_repo: ITrackRepository, media_source_repo: IMediaSourceRepository, user_repo: IUserRepository) -> None:
        self.track_repo = track_repo
        self.user_repo = user_repo
        self.media_source_repo = media_source_repo

    def execute(self, dto: TrackInDTO):
        user = self.user_repo.find_by_id(dto.user)
        if not user:
            raise UserNotFoundException('user not found')

        media_source = self.media_source_repo.find_by_id(dto.media_source)
        if not media_source:
            raise NotFoundMediaSourceException('media source not found')

        if media_source.status != StatusMusic.ready:
            raise FailedDownloadMusicException('failed music download')

        track = TrackEntity(
            user=user.id,
            media_source=media_source.id, 
            custom_title=dto.custom_title
        )

        self.track_repo.save(track)
        return TrackOutDTO.from_domain(track)


class ListTrackByUserUseCase:
    def __init__(self, track_repo: ITrackRepository) -> None:
        self.track_repo = track_repo

    def execute(self, user: UUID):
        tracks = self.track_repo.list_track_by_user(user)
        if not tracks:
            return []

        return [
            TrackOutDTO.from_domain(track)
            for track in tracks
        ]
