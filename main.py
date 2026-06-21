import requests

video_url = "https://youtu.be/Az3fs-Vq2Cc?si=A86ptT1fnRG-z7tp"
nome_arquivo = "video_baixado.mp4"

# Baixando o vídeo em partes (chunks) para não sobrecarregar a memória
with requests.get(video_url, stream=True) as r:
    r.raise_for_status()
    with open(nome_arquivo, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

print("Download concluído!")
