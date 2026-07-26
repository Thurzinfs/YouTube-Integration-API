from uuid import UUID

from app.accounts.domain.exceptions import UserNotFoundException
from app.accounts.domain.repositories import IUserRepository
from app.music.domain.exceptions import FailedDownloadMusicException, NotFoundMediaSourceException
from app.music.domain.repositories import IMediaSourceRepository
from app.music.domain.roles import StatusMusic
from app.playlist.application.dto import PlaylistInDTO, PlaylistOutDTO, PlaylistTrackInDTO, PlaylistTrackOutDTO, PlaylistUpdateDTO, TrackInDTO, TrackOutDTO
from app.playlist.domain.entities import PlaylistEntity, PlaylistTrackEntity, TrackEntity
from app.playlist.domain.exceptions import ConflictFieldException, PlaylisTrackAlreadyExistsException, PlaylistIsDeletedException, PlaylistNotFoundException, TrackNotFoundException
from app.playlist.domain.repositories import IPlaylistRepository, IPlaylistTrackRepository, ITrackRepository
from core.exceptions import BaseDomainException


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


class RegisterPlaylistTrackUseCase:
    def __init__(self, playlist_repo: IPlaylistRepository, user_repo: IUserRepository, track_repo: ITrackRepository, playlist_track_repo: IPlaylistTrackRepository) -> None:
        self.playlist_repo = playlist_repo
        self.user_repo = user_repo
        self.track_repo = track_repo
        self.playlist_track_repo = playlist_track_repo

    def execute(self, user: UUID, dto: PlaylistTrackInDTO):
        playlist = self.playlist_repo.find_by_id(dto.playlist)
        if not playlist:
            raise PlaylistNotFoundException('playlist not found')

        if playlist.user != user:
            raise  BaseDomainException("permission denied")

        track = self.track_repo.find_by_id(dto.track)
        if not track:
            raise TrackNotFoundException('track not found')

        if track.user != user:
            raise  BaseDomainException("permission denied")

        if self.playlist_track_repo.verify_exists_playlist_track_by_playlist_track(dto.track, dto.playlist):
            raise PlaylisTrackAlreadyExistsException("playlist track already exists")

        position = self.playlist_track_repo.count_all_playlist_track(dto.playlist)

        playlist_track = PlaylistTrackEntity(
            playlist=dto.playlist,
            track=dto.track,
            position=position + 1
        )

        self.playlist_track_repo.save(playlist_track)
        return PlaylistTrackOutDTO.from_domain(playlist_track)
