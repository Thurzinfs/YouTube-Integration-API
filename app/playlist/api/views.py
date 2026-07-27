from typing import List
from uuid import UUID

from ninja import Router

from app.playlist.api.dependencies import PlaylistModuleContainer
from app.playlist.api.schemas import PlaylistIn, PlaylistOut

from django.db.transaction import atomic


router_playlist = Router()

container = PlaylistModuleContainer()


@router_playlist.post('/', response={201: PlaylistOut})
@atomic
def register_playlist(request, data: PlaylistIn):
    dto = data.to_dto()

    use_case = container.register_playlist_use_case()

    playlist = use_case.execute(dto)

    return 201, PlaylistOut.from_domain(playlist)


@router_playlist.get('/list', response={200: List[PlaylistOut]})
def list_playlist(request, user_id: UUID):
    use_case = container.list_playlist_by_user_use_case()

    playlists = use_case.execute(user_id)

    return 200, [
        PlaylistOut.from_domain(playlist)
        for playlist in playlists
    ]


@router_playlist.get('/{id}', response={200: PlaylistOut})
def response_playlist(request, id: UUID):
    use_case = container.response_playlist_use_case()

    playlist = use_case.execute(id)

    return 200, PlaylistOut.from_domain(playlist)
