import os
import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp

def download_video(url, path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download completed!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def search_and_download(save_path):
    query = entry.get()
    if not query:
        messagebox.showerror("Error", "Please enter a song name.")
        return
    ydl_opts = {
        'default_search': 'ytsearch',
        'max_downloads': 1,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in result and len(result['entries']) > 0:
                video_url = result['entries'][0]['webpage_url']
                download_video(video_url, save_path)
            else:
                messagebox.showerror("Error", "No results found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def save_as():
    save_path = filedialog.askdirectory()
    if save_path:
        search_and_download(save_path)

# Set up the GUI
root = tk.Tk()
root.title("YouTube Downloader")

frame = tk.Frame(root)
frame.pack(pady=20)

label = tk.Label(frame, text="Enter song name:")
label.pack(side=tk.LEFT, padx=5)

entry = tk.Entry(frame, width=50)
entry.pack(side=tk.LEFT, padx=5)

button = tk.Button(frame, text="Save As and Download", command=save_as)
button.pack(side=tk.LEFT, padx=5)

root.mainloop()
