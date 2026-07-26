from uuid import UUID

from app import music
from app.accounts.domain.exceptions import UserNotFoundException
from app.accounts.domain.repositories import IUserRepository
from app.music.application.dto import MediaSourceOutDTO
from app.music.domain.exceptions import FailedDownloadMusicException, NotFoundMediaSourceException
from app.music.domain.repositories import IMediaSourceRepository
from app.music.domain.roles import StatusMusic
from app.playlist.application.dto import PlaylistInDTO, PlaylistOutDTO, PlaylistTrackInDTO, PlaylistTrackOutDTO, PlaylistUpdateDTO, TrackInDTO, TrackOutDTO
from app.playlist.domain.entities import PlaylistEntity, PlaylistTrackEntity, TrackEntity
from app.playlist.domain.exceptions import ConflictFieldException, PlaylisTrackAlreadyExistsException, PlaylistIsDeletedException, PlaylistNotFoundException, PlaylistTrackNotFoundException, TrackNotFoundException
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


class ListMusicsInPlaylistTrack:
    def __init__(self, playlist_track_repo: IPlaylistTrackRepository, track_repo: ITrackRepository, music_repo: IMediaSourceRepository) -> None:
        self.playlist_track_repo = playlist_track_repo
        self.track_repo = track_repo
        self.music_repo = music_repo

    def execute(self, playlist: UUID):
        playlist_track = self.playlist_track_repo.list_musics_whithin_playlist(playlist)
        if not playlist_track:
            raise BaseDomainException("playlist track not found")

        track_ids = [pt.track for pt in playlist_track if pt.track is not None]

        tracks = self.track_repo.find_many_by_ids(track_ids)
        tracks_by_id = {track.id: track for track in tracks}

        media_sources_id = [track.media_source for track in tracks if track.media_source is not None]

        media_source = self.music_repo.find_many_by_ids(media_sources_id)
        media_source_by_id = {ms.id: ms for ms in media_source}

        musics = []
        for pt in playlist_track:
            track = tracks_by_id.get(pt.track)  # type: ignore
            if track is None:
                continue

            media_source = media_source_by_id.get(track.media_source)  # type: ignore
            if media_source is None:
                continue 

            musics.append(media_source)

        return [
            MediaSourceOutDTO.from_domain(music)
            for music in musics
        ]


class RemoveMusicInPlaylist:
    def __init__(self, playlist_track_repo: IPlaylistTrackRepository, track_repo: ITrackRepository) -> None:
        self.playlist_track_repo = playlist_track_repo
        self.track_repo = track_repo

    def execute(self, user: UUID, playlist_track_id: UUID):
        playlist_track = self.playlist_track_repo.find_by_id(playlist_track_id)
        if not playlist_track:
            raise PlaylistTrackNotFoundException('playlist track not found')

        if playlist_track.track is None:
            raise BaseDomainException('playlist track has no track')

        track = self.track_repo.find_by_id(playlist_track.track)
        if not track:
            raise TrackNotFoundException('track not found')

        if track.user != user:
            raise BaseDomainException('user unauthorized')

        self.playlist_track_repo.delete_by_id(playlist_track.id)


class RemoveMusicInTrack:
    def __init__(self, track_repo: ITrackRepository) -> None:
        self.track_repo = track_repo

    def execute(self, user: UUID, track_id: UUID):
        track = self.track_repo.find_by_id(track_id)
        if not track:
            raise TrackNotFoundException('track not found')

        if track.user != user:
            raise BaseDomainException('user unauthorized')

        self.track_repo.delete_by_id(track.id)
