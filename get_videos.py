import random
from concurrent.futures.thread import ThreadPoolExecutor

import scrapetube
import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
from random_word import RandomWords


def get_random_video(choice):
    query = random.choice(choice)
    videos = scrapetube.get_search(query, limit=50)
    video_list = list(videos)
    if video_list:
        selected_video = random.choice(video_list)
        video_id = selected_video['videoId']
        return f'https://www.youtube.com/watch?v={video_id}'
    else:
        return None


def download_video(url,dir):
    yt = YouTube(url)
    video = yt.streams.filter(file_extension='mp4').first()
    filename = video.download(dir)
    return filename


def extract_audio(filename,dir,i, duration=1):
    with VideoFileClip(filename) as video:
        start_time = random.randint(0, int(video.duration) - duration)
        end_time = start_time + duration
        audio_clip = video.subclip(start_time, end_time).audio
        audio_clip.write_audiofile(dir+"/sample"+str(i)+".mp3")

def do_shit(choice,dir, i):
    try:
        url = get_random_video(choice)
        if url:
            print(f"Downloading video from {url}")
            filename = download_video(url,dir)
            extract_audio(filename,dir,i)
            os.remove(filename)
        else:
            print("Failed to get a random video.")
    except:
        return

def main():
    print("MAKING SOMETHING SPICY")

    print("10 RANDOM MUSIC SAMPLES")
    choice = ["dnb", "garage", "house", "afro", "glitchpop", "breakcore", "housecore"]
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(do_shit,choice,"beats",i) for i in range(10)]
        for future in futures:
            future.result()

    print("10 RANDOM WACK SAMPLES")
    r = RandomWords()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(do_shit,[ r.get_random_word(), r.get_random_word(), r.get_random_word(), r.get_random_word()],"random",i) for i in range(10)]
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
