import os
import yt_dlp
from pydub import AudioSegment

def download_videos(singer_name, num_videos, cookie_path):
    # Define options for yt-dlp
    options = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',  # Output file naming
        'cookies': cookie_path,  # Use cookies to bypass sign-in
    }
    
    search_url = f"ytsearch{num_videos}:{singer_name}"
    
    with yt_dlp.YoutubeDL(options) as ydl:
        try:
            # Download audio files
            ydl.download([search_url])
            print(f"Successfully downloaded {num_videos} videos for {singer_name}.")
        except Exception as e:
            print(f"An error occurred while downloading: {e}")

def convert_to_audio(file_name):
    """Convert video file to audio using pydub."""
    if not file_name.endswith('.mp4'):
        print(f"Skipping conversion for {file_name}. Not an MP4 file.")
        return

    audio_file_name = f"{os.path.splitext(file_name)[0]}.mp3"
    
    # Convert video to audio
    try:
        video = AudioSegment.from_file(file_name, format='mp4')
        video.export(audio_file_name, format='mp3')
        print(f"Converted {file_name} to {audio_file_name}.")
        return audio_file_name
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

def cut_audio(file_name, start_time, end_time):
    """Cut audio file between start_time and end_time (in milliseconds)."""
    try:
        audio = AudioSegment.from_file(file_name)
        cut_audio = audio[start_time:end_time]
        cut_audio_name = f"cut_{os.path.basename(file_name)}"
        cut_audio.export(cut_audio_name, format='mp3')
        print(f"Cut audio file saved as {cut_audio_name}.")
        return cut_audio_name
    except Exception as e:
        print(f"An error occurred while cutting the audio: {e}")

def merge_audios(audio_files, output_file_name):
    """Merge multiple audio files into one."""
    try:
        combined = AudioSegment.empty()
        for file_name in audio_files:
            audio = AudioSegment.from_file(file_name)
            combined += audio
        combined.export(output_file_name, format='mp3')
        print(f"Merged audio files into {output_file_name}.")
    except Exception as e:
        print(f"An error occurred while merging audio files: {e}")

def main():
    # Define the singer name and number of videos to download
    singer_name = "Sharry Mann"  # Change to the desired artist's name
    num_videos = 5  # Change to the number of videos you want to download
    cookie_path = "path/to/cookies.txt"  # Specify the path to your cookies.txt file

    # Check if cookies file exists
    if not os.path.exists(cookie_path):
        print(f"Cookies file not found at {cookie_path}. Please ensure the path is correct.")
        return

    # Call the download function
    download_videos(singer_name, num_videos, cookie_path)

    # Convert downloaded videos to audio
    audio_files = []
    for file in os.listdir():
        if file.endswith('.mp4'):
            audio_file = convert_to_audio(file)
            if audio_file:
                audio_files.append(audio_file)

    # Cut the first audio file (modify times as needed)
    if audio_files:
        cut_audio_file = cut_audio(audio_files[0], 10000, 30000)  # Cut from 10s to 30s

    # Merge all audio files into one
    merge_audios(audio_files, 'merged_audio.mp3')

if __name__ == "__main__":
    main()
