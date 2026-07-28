from typing import List
from uuid import UUID

from ninja import Router

from app.accounts.api.auth import AuthBearer
from app.music.api.schemas import MediaSourceOut
from app.playlist.api.dependencies import PlaylistModuleContainer
from app.playlist.api.schemas import PlaylistIn, PlaylistOut, PlaylistTrackIn, PlaylistTrackOut, TrackIn, TrackOut

from django.db.transaction import atomic


router_playlist = Router()

track_router = Router()

playlist_track_router = Router()

container = PlaylistModuleContainer()


@router_playlist.post('/', response={201: PlaylistOut}, auth=AuthBearer())
@atomic
def register_playlist(request, data: PlaylistIn):
    dto = data.to_dto()

    use_case = container.register_playlist_use_case()

    playlist = use_case.execute(dto)

    return 201, PlaylistOut.from_domain(playlist)


@router_playlist.get('/list', response={200: List[PlaylistOut]}, auth=AuthBearer())
def list_playlist(request):
    use_case = container.list_playlist_by_user_use_case()

    playlists = use_case.execute(request.auth.id)

    return 200, [
        PlaylistOut.from_domain(playlist)
        for playlist in playlists
    ]


@router_playlist.get('/musics/{id}', response={200: List[MediaSourceOut]}, auth=AuthBearer())
def list_musics_in_playlist(request, id: UUID):
    use_case = container.list_musics_in_playlist_use_case()

    musics = use_case.execute(id)

    return 200, [
        MediaSourceOut.from_domain(music)
        for music in musics
    ]


@router_playlist.get('/{id}', response={200: PlaylistOut}, auth=AuthBearer())
def response_playlist(request, id: UUID):
    use_case = container.response_playlist_use_case()

    playlist = use_case.execute(id)

    return 200, PlaylistOut.from_domain(playlist)


@track_router.post('/', response={201: TrackOut}, auth=AuthBearer())
@atomic
def register_track(request, data: TrackIn):
    dto = data.to_dto()

    use_case = container.register_track_use_case()

    track = use_case.execute(dto)

    return 201, TrackOut.from_domain(track)


@track_router.get('/{id}', response={200: List[TrackOut]}, auth=AuthBearer())
def list_track(request):
    use_case = container.list_track_use_case()

    tracks = use_case.execute(request.auth.id)

    return 200, [
        TrackOut.from_domain(track)
        for track in tracks
    ]


@playlist_track_router.post('/', response={201: PlaylistTrackOut}, auth=AuthBearer())
@atomic
def regiter_playlist_track(request, data: PlaylistTrackIn):
    dto = data.to_dto()

    use_case = container.register_playlist_track_use_case()

    playlist_track = use_case.execute(request.auth.id, dto)

    return 201, PlaylistTrackOut.from_domain(playlist_track)
