import shutil
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from moviepy.editor import VideoFileClip
from pytube import YouTube
from tkinter import filedialog
import urllib.request, io
import moviepy as mp
import re
import os
import threading


def select_path():
    path = filedialog.askdirectory()
    path_label.config(text=path)


def download_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    download_percentage = (bytes_downloaded / total_size) * 100
    progress_bar['value'] = download_percentage
    root.update_idletasks()


def download_video(video_link):
    user_path = path_label.cget("text")
    root.title("Downloading...")

    yt = YouTube(video_link, on_progress_callback=download_progress)
    raw_data = urllib.request.urlopen(yt.thumbnail_url).read()
    im = Image.open(io.BytesIO(raw_data)).resize((200, 200))
    image = ImageTk.PhotoImage(im)
    label = tk.Label(image=image)
    label.image = image
    canvas.create_window(450, 450, window=label)

    author = tk.Label(text=yt.author)
    canvas.create_window(80, 380, window=author)

    titl = tk.Label(text=yt.title)
    canvas.create_window(120, 360, window=titl)

    vid_lenght = tk.Label(text=yt.length)
    canvas.create_window(80, 400, window=vid_lenght)

    stream = yt.streams.get_highest_resolution()
    t = threading.Thread(target=download_video_thread, args=(stream, user_path))
    t.start()


def download_video_thread(stream, user_path):
    stream.download(user_path)
    root.title("Download Complete! Download another file...")
    progress_bar['value'] = 0


def download_audio(video_link):
    user_path = path_label.cget("text")
    root.title("Downloading...")

    yt = YouTube(video_link, on_progress_callback=download_progress)
    ys = yt.streams.filter(only_audio=True).first().download(user_path)

    root.title('Converting file')
    for file in os.listdir(user_path):
        if re.search('mp4', file):
            mp4_path = os.path.join(user_path, file)
            mp3_path = os.path.join(user_path, os.path.splitext(file)[0] + '.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)
            os.remove(mp4_path)

    root.title("Download Complete! Download another file...")
    progress_bar['value'] = 0


root = tk.Tk()
title = root.title("NoAD Downloader")
canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()
root.resizable(False, False)

logo_text = tk.Label(text="NoAD Downloader", font=('Arial', 20), bg=None)
logo_text.pack()


link_field = tk.Entry(root, width=50)
link_label = tk.Label(root, text="Video link: ", font=('Arial', 10)).place(x=76, y=190, width=70, height=20)

path_label = tk.Label(root, text="Select path for download", font=("Arial", 12))
path_label.config(bg="#FFF")
canvas.create_window(300, 250, window=path_label)
select_btn = tk.Button(root, text="Select", command=select_path)
canvas.create_window(300, 280, window=select_btn)

canvas.create_window(115, 200, window=link_label)
canvas.create_window(300, 200, window=link_field)

download_btn = tk.Button(root, text="Download Video", command=lambda: download_video(link_field.get()))
download_audio_btn = tk.Button(root, text="Download Audio", command=lambda: download_audio(link_field.get()))
canvas.create_window(530, 200, window=download_btn)
canvas.create_window(530, 170, window=download_audio_btn)

progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')
canvas.create_window(300, 500, window=progress_bar)

root.mainloop()
