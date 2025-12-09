import streamlit as st
import yt_dlp
import os

# Configuração da Página
st.set_page_config(page_title="MP3 Downloader", layout="centered")

st.title("🎵 YouTube para MP3")
st.write("Cole o link do vídeo abaixo para baixar o áudio.")

# Campo para o Link
url = st.text_input("Link do YouTube:")

def baixar_audio(video_url):
    # Opções do yt-dlp para baixar apenas áudio e converter para mp3
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        # AQUI ESTÁ O TRUQUE PARA TENTAR EVITAR O ERRO 403:
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            # Ajusta a extensão para mp3 (já que o FFmpeg converteu)
            final_filename = filename.rsplit('.', 1)[0] + '.mp3'
            return final_filename, info['title']
    except Exception as e:
        return None, str(e)

if st.button("🚀 Converter e Baixar"):
    if url:
        with st.spinner('Baixando e convertendo... (isso pode levar alguns segundos)'):
            # Cria a pasta downloads se não existir
            if not os.path.exists('downloads'):
                os.makedirs('downloads')
            
            file_path, title_or_error = baixar_audio(url)

            if file_path:
                st.success(f"Sucesso! Áudio extraído: {title_or_error}")
                
                # Botão para fazer o download do arquivo para o celular/pc
                with open(file_path, "rb") as file:
                    st.download_button(
                        label="⬇️ Baixar MP3",
                        data=file,
                        file_name=f"{title_or_error}.mp3",
                        mime="audio/mpeg"
                    )
                
                # Opcional: Limpar o arquivo do servidor depois (para economizar espaço)
                # os.remove(file_path) 
            else:
                st.error(f"Erro ao baixar: {title_or_error}")
    else:
        st.warning("Por favor, insira um link válido.")
