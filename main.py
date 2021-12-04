from tkinter import *
from tkinter import filedialog
import ffmpeg
import os
import subprocess
import glob
import torch

supported_formats = ('*.mp4', '*.mkv', '*.avi', '*.mov', "*.mp3", "*.wav", "*.flac", "*.ogg", "*.m4a")
files=[]

def getDirectory():
    global filepath
    filepath = filedialog.askdirectory(initialdir = "/",title = "Select directory")
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)
    listSupportedFormatsFiles()

def playVideo(filename=""):
    subprocess.call(["ffplay", filename])

def frameInterpolation():
    print(filename, output_file_name)
    quoted_filename = f'"{filename}"'
    quoted_output_file_name = f'"{output_file_name}"'
    slomo_directory = '"' + os.getcwd() + "\\slowmo\\video_to_slomo.py" + '"'
    ckpt_directory = '"' + os.getcwd() + "\\slowmo\\SuperSloMo.ckpt" + '"'
    slowmo_command = "python " + slomo_directory + " --video " + quoted_filename + " --sf 3 --checkpoint " + ckpt_directory + " --fps 60 --output " + quoted_output_file_name + " --batch_size 4"
    print(slowmo_command)
    subprocess.call(slowmo_command, shell=True)
    #subprocess.call(["python slowmo\video_to_slomo.py --ffmpeg C:\Users\Gerald\SloMo\ffmpeg\bin\ --video", filename," --sf 4 --checkpoint slowmo\SuperSloMo.ckpt --fps 120 --output ", output_file_name, " --batch_size 1"])

def listSupportedFormatsFiles():
    print(filepath)
    list_box.delete(0, END)
    for format in supported_formats:
        for file in glob.glob(filepath+"/"+format):
            files.append(file)
            list_box.insert(END, file)

def playSelectedFiles(event):
    global selected_files
    global output_file_name
    global filename
    index = list_box.curselection()
    print(index)
    selected_files = list_box.get(index)
    print(selected_files)
    filename = selected_files
    output_file_name = selected_files.split(".")[0] + "_inter_.mkv"
    playVideo(selected_files)

window = Tk()
window.geometry('800x800')
window.title("Gareeb Player")
window.configure(background='#4c4c4c')
label_file_explorer = Label(window, text="Gareeb Music Player", font=("Arial Bold", 20), fg='#000000', bg='#4c4c4c')
button_for_directory = Button(window, text="Select Directory", command=getDirectory)
button_to_exit = Button(window, text="Exit", command=exit)
list_box = Listbox(window, width=100, height=20, selectmode=SINGLE)
list_box.bind('<Double-1>', playSelectedFiles)
button_to_call_interpolation = Button(window, text="SlowMo", command=frameInterpolation)
label_file_explorer.grid(column = 1, row = 1)
button_for_directory.grid(column = 1, row = 2)
list_box.grid(column = 1, row = 3)
button_to_call_interpolation.grid(column = 1, row = 4)
button_to_exit.grid(column = 1,row = 5)
window.mainloop()