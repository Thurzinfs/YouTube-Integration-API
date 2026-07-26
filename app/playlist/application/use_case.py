from uuid import UUID

from app.accounts.domain.exceptions import UserNotFoundException
from app.accounts.domain.repositories import IUserRepository
from app.playlist.application.dto import PlaylistInDTO, PlaylistOutDTO, PlaylistUpdateDTO
from app.playlist.domain.entities import PlaylistEntity
from app.playlist.domain.exceptions import ConflictFieldException, PlaylistIsDeletedException, PlaylistNotFoundException
from app.playlist.domain.repositories import IPlaylistRepository


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
    