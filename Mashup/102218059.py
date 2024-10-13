import sys
import os
from pytube import YouTube
from pydub import AudioSegment
from pydub.playback import play

def download_videos(singer_name, num_videos):
    videos = []
    for i in range(num_videos):
        # You can modify this URL pattern based on how you want to search for the singer
        search_url = f"https://www.youtube.com/results?search_query={singer_name.replace(' ', '+')}"
        yt = YouTube(search_url)  # Directly fetching from YouTube search results
        video = yt.streams.filter(only_audio=True).first()
        videos.append(video.download(filename=f"{singer_name}_{i}.mp4"))
    return videos

def convert_to_audio(videos):
    audio_files = []
    for video in videos:
        audio_file = f"{os.path.splitext(video)[0]}.mp3"
        audio_segment = AudioSegment.from_file(video)
        audio_segment.export(audio_file, format="mp3")
        audio_files.append(audio_file)
    return audio_files

def cut_audio(audio_files, duration):
    cut_audio_files = []
    for audio_file in audio_files:
        audio_segment = AudioSegment.from_file(audio_file)
        cut_audio = audio_segment[:duration * 1000]  # Convert duration to milliseconds
        cut_file = f"cut_{os.path.basename(audio_file)}"
        cut_audio.export(cut_file, format="mp3")
        cut_audio_files.append(cut_file)
    return cut_audio_files

def merge_audios(cut_audio_files, output_file):
    combined = AudioSegment.empty()
    for audio_file in cut_audio_files:
        audio_segment = AudioSegment.from_file(audio_file)
        combined += audio_segment
    combined.export(output_file, format="mp3")

def main():
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer_name = sys.argv[1]
    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("Number of videos and audio duration must be integers.")
        sys.exit(1)

    output_file = sys.argv[4]

    if num_videos <= 10:
        print("Number of videos must be greater than 10.")
        sys.exit(1)

    if duration <= 20:
        print("Audio duration must be greater than 20 seconds.")
        sys.exit(1)

    try:
        # Step 1: Download videos
        videos = download_videos(singer_name, num_videos)

        # Step 2: Convert videos to audio
        audio_files = convert_to_audio(videos)

        cut_audio_files = cut_audio(audio_files, duration)

        merge_audios(cut_audio_files, output_file)

        print(f"Merged audio saved as {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
