from typing import List
from uuid import UUID

from ninja import Router

from app.music.api.dependencies import MusicContainer
from app.music.api.schemas import MediaSourceIn, MediaSourceOut

from django.db.transaction import atomic


router = Router()

container = MusicContainer()


@router.post('/', response={201: MediaSourceOut})
@atomic
def register_music(request, data: MediaSourceIn):
    dto = data.to_dto()

    use_case = container.start_register_music_use_case()

    music = use_case.execute(dto)

    return MediaSourceOut.from_domain(music)


@router.get('/lists', response={200: List[MediaSourceOut]})
def list_musics(request):
    use_case = container.list_musics_actives_use_case()

    musics = use_case.execute()

    return 200, [
        MediaSourceOut.from_domain(music)
        for music in musics
    ]


@router.get('/{id}', response={200: MediaSourceOut})
def response_music(request, id: UUID):
    use_case = container.response_music_use_case()

    music = use_case.execute(id)

    return MediaSourceOut.from_domain(music)


@router.get("/musicas/buscar", response=List[MediaSourceOut])
def search_musics(request, term: str):
    use_case = container.search_musics_by_similarity_use_case()

    musics = use_case.execute(term)

    return [
        MediaSourceOut.from_domain(dto)
        for dto in musics
    ]


@router.delete('/{id}', response={200: MediaSourceOut})
@atomic
def deactive_music(request, id: UUID):
    use_case = container.deactive_music_use_case()

    music = use_case.execute(id)

    return MediaSourceOut.from_domain(music)
