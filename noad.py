from distutils.cmd import Command
from pytube import YouTube
from tkinter import *
from tkinter import ttk
import moviepy
import moviepy.editor as mp
import re
import os
import io
import time
from pytube.cli import on_progress
from tkinter import ttk,messagebox
from PIL import Image, ImageTk 
from urllib.request import urlopen

menu_inicial = Tk()











menu_inicial.title('NoAD')

menu_inicial.geometry('400x400')
menu_inicial.resizable(False, False)


urlEntry = Entry(menu_inicial)

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 

def link():
    
    
    Label(menu_inicial, text="URL: ", background='#ddd', foreground="#009", anchor=W).place(x=100, y= 100, width=50, height=25)
    
    urlEntry.place(x = 150, y= 100, width=150,height=25)

    Button(menu_inicial, text='Baixar', command=download).place(x=180, y=140, width=40, height=25)

    btn.pack_forget()




def download():

    

    link = urlEntry.get()

    path = desktop
    print("Baixando...")
    
    yt = YouTube(link)

    imageUrl = yt.thumbnail_url
    u = urlopen(imageUrl)
    raw_data = u.read()
    u.close()


    tkimage = ImageTk.PhotoImage(data=raw_data)
    l2 = Label(image=tkimage).place(x=250,y=250,width=50,height=50)
    l2.image = tkimage
    



    ys = yt.streams.filter(only_audio=True).first().download(path)
    print("Download completo!")

    print('Convertento arquivo')
    for file in os.listdir(path):
        if re.search('mp4', file):
            mp4_path = os.path.join(path, file)
            mp3_path = os.path.join(path, os.path.splitext(file)[0] + '.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)
            os.remove(mp4_path)


    ttk.Label(menu_inicial, text="Download completo!!!", background='#ddd', foreground="#009", anchor=CENTER).place(x=120, y= 170, width=150, height=30)

ttk.Progressbar        


btn = Button(menu_inicial, text= "Iniciar", command=link, width=10, height=5)
btn.pack(pady=150)


menu_inicial.mainloop()




