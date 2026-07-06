from typing import cast
from uuid import UUID

from celery import shared_task
import yt_dlp

from django.conf import settings

from app.music.application.dto import FinishDownloadMusicDTO

import os


@shared_task
def download_music(id: UUID, url: str) -> None:
    from app.music.api.dependencies import MusicContainer

    relative_subdir = "music"

    disk_dir = os.path.join(settings.MEDIA_ROOT, relative_subdir)
    os.makedirs(disk_dir, exist_ok=True)

    output_template = os.path.join(disk_dir, f"{id}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',  
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio', 
            'preferredcodec': 'mp3',     
            'preferredquality': '192',  
        }],
        'outtmpl': output_template, 
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
            
            info_dict = ydl.extract_info(url, download=True)

            if not info_dict:
                raise ValueError("yt-dlp não retornou informações do vídeo")

            title = cast(str, info_dict.get('title', ''))
            uploader = cast(str, info_dict.get('uploader', ''))
            duration = cast(int, info_dict.get('duration', 0))

            saved_path = f"{relative_subdir}/{id}.mp3"
            
            repo = MusicContainer.music_repo()

            use_case = MusicContainer.finish_download_music_use_case()

            media = repo.find_by_id(id)

            if not media:
                return None
            
            dto = FinishDownloadMusicDTO(
                id=id,
                title=title,
                channel_name=uploader,
                duration_seconds=duration,
                audio_file_path=saved_path,
            )

            use_case.execute(dto)
            
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
