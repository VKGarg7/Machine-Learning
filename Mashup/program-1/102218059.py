import sys
from pytube import YouTube
from youtubesearchpython import VideosSearch
from moviepy.editor import concatenate_audioclips, AudioFileClip

def download_videos(singer_name, num_videos):
    search_query = f"{singer_name} songs"
    print(f"Searching for {num_videos} videos of {singer_name}...")

    # YouTube search function and download
    videos_search = VideosSearch(search_query, limit=num_videos)
    results = videos_search.next()

    # Print the entire results response for debugging
    print("Search results:", results)  

    # Check if 'result' is in the response
    if 'result' in results:
        video_urls = [result['link'] for result in results['result']]
    else:
        print("No results found or invalid response.")
        return []

    if not video_urls:
        print("No video URLs found.")
        return []

    video_paths = []
    for idx, video_url in enumerate(video_urls):
        try:
            yt = YouTube(video_url)
            print(f"Downloading {yt.title}...")
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            if stream:
                video_file = f"{singer_name}_video_{idx + 1}.mp4"
                stream.download(filename=video_file)
                video_paths.append(video_file)
            else:
                print(f"Stream not found for video: {video_url}")
        except Exception as e:
            print(f"An error occurred while downloading: {e}")

    return video_paths

def convert_to_audio(video_paths):
    audio_paths = []
    for video_path in video_paths:
        try:
            yt_video = AudioFileClip(video_path)
            audio_file = video_path.replace('.mp4', '.mp3')
            yt_video.write_audiofile(audio_file)
            audio_paths.append(audio_file)
            yt_video.close()
            print(f"Converted {video_path} to {audio_file}.")
        except Exception as e:
            print(f"An error occurred during conversion: {e}")

    return audio_paths

def cut_audio(audio_paths, cut_duration):
    cut_audio_paths = []
    for audio_path in audio_paths:
        try:
            audio_clip = AudioFileClip(audio_path)
            cut_audio_file = audio_path.replace('.mp3', f'_cut.mp3')
            cut_audio = audio_clip.subclip(0, cut_duration)
            cut_audio.write_audiofile(cut_audio_file)
            cut_audio_paths.append(cut_audio_file)
            audio_clip.close()
            print(f"Cut audio file created: {cut_audio_file}.")
        except Exception as e:
            print(f"An error occurred while cutting audio: {e}")

    return cut_audio_paths

def merge_audios(cut_audio_paths, output_file):
    try:
        audio_clips = [AudioFileClip(audio) for audio in cut_audio_paths]
        final_clip = concatenate_audioclips(audio_clips)
        final_clip.write_audiofile(output_file)
        for clip in audio_clips:
            clip.close()
        final_clip.close()
        print(f"Merged audio saved as {output_file}.")
    except Exception as e:
        print(f"An error occurred while merging audios: {e}")

def main():
    # Check for the correct number of parameters
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    # Read command line arguments
    singer_name = sys.argv[1]
    try:
        num_videos = int(sys.argv[2])
        audio_duration = int(sys.argv[3])
    except ValueError:
        print("Number of videos and audio duration must be integers.")
        sys.exit(1)

    output_file_name = sys.argv[4]

    # Check for valid input values
    if num_videos <= 10:
        print("Number of videos must be greater than 10.")
        sys.exit(1)

    if audio_duration <= 20:
        print("Audio duration must be greater than 20 seconds.")
        sys.exit(1)

    # Main processing steps
    video_paths = download_videos(singer_name, num_videos)
    if not video_paths:
        print("No videos downloaded. Exiting.")
        sys.exit(1)

    audio_paths = convert_to_audio(video_paths)
    cut_audio_paths = cut_audio(audio_paths, audio_duration)
    merge_audios(cut_audio_paths, output_file_name)

if __name__ == "__main__":
    main()

