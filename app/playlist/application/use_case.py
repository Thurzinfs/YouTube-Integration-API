from app.accounts.domain.exceptions import UserNotFoundException
from app.accounts.domain.repositories import IUserRepository
from app.playlist.application.dto import PlaylistInDTO, PlaylistOutDTO
from app.playlist.domain.entities import PlaylistEntity
from app.playlist.domain.exceptions import ConflictFieldException
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
 