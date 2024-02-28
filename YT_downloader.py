import customtkinter as ctk
from tkinter import ttk
from pytube import YouTube,Playlist
from yt_dlp import YoutubeDL
import os
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context



# Resolutions are fetched
def sort_key(string):
    # Extract the numeric prefix from the string
    numeric_prefix = int(''.join(filter(str.isdigit, string)))
    return numeric_prefix



def select_res():

    try:
        url = entry_url.get()
        yt=YouTube(url,on_progress_callback=progress)
        # list_resolution =[int(i.split("p")[0]) for i in (list(dict.fromkeys([i.resolution for i in yt.streams if i.resolution])))]
        list_resolution =list(dict.fromkeys([i.resolution for i in yt.streams if i.resolution]))
        list_resolution.sort(key=sort_key)
        print(list_resolution)
        resolution_combobox.configure(values=list_resolution)
        resolution_combobox.pack(pady=(10,5))
        resolution_combobox.set(list_resolution[0])
    except Exception as e:
        print(type(e))
        print(e)
        status_label.configure(text=f"Error: {str(e)}",text_color="white", fg_color="red")




def sanitize_filename(filename):
    disallowed_chars = ['?', '>', '<', '|', ':', '*', '/', '\\', '"']
    sanitized_filename = filename
    for char in disallowed_chars:
        sanitized_filename = sanitized_filename.replace(char, '-')
    return sanitized_filename




def download_playlist(playlist_url, output_dir):
    try:
        playlist = Playlist(playlist_url)
        print(f"Downloading playlist: {playlist.title}")
        for video in playlist.videos:
            download_video(video.watch_url, output_dir)
    except Exception as e:
        print(f"Error downloading playlist: {str(e)}")

def download_video():
    url = entry_url.get()
    # print(url)
    resolution=resolution_var.get()
    print(f"Resolution selected : {resolution}")
    progressbar_label.pack(pady=(10,5))
    progressbar.pack(pady=(10,5))
    status_label.pack(pady=(10,5))
    try:
        yt=YouTube(url,on_progress_callback=progress)
        stream=yt.streams.filter(res=resolution).first()
        # print(list_resolution)
        download_dir = "C:\\Users\\devba\\Downloads"
        
        file_name = f"{stream.title} - {resolution}.mp4"
        download_path = os.path.join(download_dir, file_name)

        file_name=sanitize_filename(file_name)

        Title.configure(text=file_name)
        Title.pack(pady=(10,5))
        Title.update()
        
        # Check if the file already exists
        count = 1
        while os.path.exists(download_path):
            # Append a sequential number to the filename
            file_name = f"{file_name} ({count}).mp4"
            download_path = os.path.join(download_dir, file_name)
            count += 1
       
        # print(download_path)
        stream.download(output_path=download_dir, filename=file_name)
        status_label.configure(text="Download Completed!",text_color="white", fg_color="green")


    except Exception as e:
        print(type(e))
        print(e)
        status_label.configure(text=f"Error: {str(e)}",text_color="white", fg_color="red")



def progress(stream, chunks, bytes_remaining):
    total_size=stream.filesize
    bytes_downloaded=total_size-bytes_remaining
    percentage_completed=(bytes_downloaded/total_size)*100
    progressbar_label.configure(text=f"{int(percentage_completed)} %")
    progressbar_label.update()

    progressbar.set(float(percentage_completed/100))


# root window
root = ctk.CTk()
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
# title of window
root.title("YouTube Downloader")


# set min and max width and height

root.geometry("720x480")
root.minsize(720, 480)
root.maxsize(width=1080, height=720)
root.option_add("*TCombobox*Listbox*Font", 20)
root.option_add("*TCombobox*Listbox.justify",ctk.CENTER)

# create a frame to hold the content
content_frame = ctk.CTkFrame(master=root)
content_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)


# create a label and the entry widget for the video url

entry_url = ctk.CTkEntry(content_frame, 400, 40, placeholder_text="Enter Youtube URL: ", justify=ctk.CENTER)
entry_url.pack(pady=(10,5))

# create a download button
Add_download_button = ctk.CTkButton(content_frame,text="Add to Download",command=select_res,corner_radius=5, fg_color="green",)
Add_download_button.pack(pady=(10,5))


download_button = ctk.CTkButton(content_frame,text="Download",command=download_video,corner_radius=5, fg_color="green")
download_button.pack(pady=(10,5))

resolution_var=ctk.StringVar()
resolution_combobox=ttk.Combobox(content_frame, state='readonly',font=14,justify="center",textvariable=resolution_var,cursor="hand2")



# create a label and the progress bar to display the download progress
progressbar_label = ctk.CTkLabel(content_frame,text="0%")
# progressbar_label.pack(pady=(10,5))

progressbar = ctk.CTkProgressBar(content_frame, width=400)
progressbar.set(0)
# progressbar.pack(pady=(10,5))

# create a status label
status_label = ctk.CTkLabel(content_frame, text="Downloaded", corner_radius=5,)
Title=ctk.CTkLabel(content_frame)

# to start the app
root.mainloop()
