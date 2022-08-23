from cgitb import text
from select import select
import shutil
from tkinter import *
from tkinter import filedialog
import tkinter
from turtle import bgcolor
from PIL import Image,ImageTk
from moviepy import *
import moviepy.editor as mp
from moviepy.editor import VideoFileClip
from pytube import YouTube
import urllib.request, io
import re, os,io

screen = Tk()
title = screen.title("NoAD")
canvas = Canvas(screen, width= 600, height= 600)
canvas.pack()
screen.resizable(False,False)

#Functions

def select_path():
    #Allows user to select a path from the explorer
    path = filedialog.askdirectory()
    path_label.config(text=path)

def download_video():
    #Get user path
    get_link = link_field.get()


    #Get selected path
    user_path = path_label.cget("text")
    screen.title("Downloading...")

    #Get thumbnail
    yt = YouTube(get_link)
    raw_data = urllib.request.urlopen(yt.thumbnail_url).read()
    im = Image.open(io.BytesIO(raw_data)).resize((200, 200))
    image = ImageTk.PhotoImage(im)
    canvas.create_image(450,450, image=image)

    #Get author
    author = Label(text=yt.author)
    canvas.create_window(80,380, window=author)

    #Get video title
    titl = Label(text=yt.title)
    canvas.create_window(120,360, window=titl)

    #Get video lenght
    vid_lenght = Label(text=yt.length)
    canvas.create_window(80,400, window=vid_lenght)


    #Download Video
    mp4_video = YouTube(get_link).streams.get_highest_resolution().download()
    vid_clip = VideoFileClip(mp4_video)
    vid_clip.close()
    #Move file to selected directory
    shutil.move(mp4_video, user_path)
    screen.title("Download Complete! Downlaod another file...")

def download_audio():
    #Get user path
    get_link = link_field.get()


    #Get selected path
    user_path = path_label.cget("text")
    screen.title("Downloading...")

    #Get thumbnail
    yt = YouTube(get_link)
    raw_data = urllib.request.urlopen(yt.thumbnail_url).read()
    im = Image.open(io.BytesIO(raw_data)).resize((200, 200))
    image = ImageTk.PhotoImage(im)
    canvas.create_image(450,450, image=image)

    #Get author
    author = Label(text=yt.author)
    canvas.create_window(80,380, window=author)

    #Get video title
    titl = Label(text=yt.title)
    canvas.create_window(120,360, window=titl)

    #Get video lenght
    vid_lenght = Label(text=yt.length)
    canvas.create_window(80,400, window=vid_lenght)


    #Download Audio

    ys = yt.streams.filter(only_audio=True).first().download(user_path)

    screen.title('Convertento arquivo')
    for file in os.listdir(user_path):
        if re.search('mp4', file):
            mp4_path = os.path.join(user_path, file)
            mp3_path = os.path.join(user_path, os.path.splitext(file)[0] + '.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)
            os.remove(mp4_path)



    #Move file to selected directory
    screen.title("Download Complete! Downlaod another file...")


    




# Logo - Imagem
logo_text = Label(text="NoAD Downloader" ,font=('Arial', 20), bg=None, anchor=N)

logo_text.pack()

logo_img = (Image.open("logo-NoAD.png"))

#Resize

resized_logo_img = logo_img.resize((615,600), Image.ANTIALIAS)
new_image= ImageTk.PhotoImage(resized_logo_img)

canvas.create_image(300, 300,image=new_image)

#Link Field

link_field = Entry(screen, width=50)
link_label = Label(screen, text = "Video link: ", font=('Arial', 10)).place(x=76,y=190,width=70, height=20)

#Select Path for saving the file

path_label = Label(screen, text= "Select path for download", font=("Arial", 12))
select_btn = Button(screen, text="Select", command=select_path)

#Add to window
path_label.config(bg="#FFF")
canvas.create_window(300, 250, window=path_label)
canvas.create_window(300, 280, window=select_btn)


#Add widgets to window

canvas.create_window(115, 200, window=link_label)
canvas.create_window(300, 200, window=link_field)

#Download Buttons

download_btn = Button(screen, text="Download Video", command=download_video)
download_audio_btn = Button(screen, text="Download Audio", command=download_audio)


#Add to canvas

canvas.create_window(530, 200, window=download_btn)
canvas.create_window(530, 170, window=download_audio_btn)






screen.mainloop()