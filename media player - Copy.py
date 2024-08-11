import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame

class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player")
        self.root.geometry("600x400")
        self.root.configure(bg='gray')

        # Initialize Pygame mixer
        pygame.mixer.init()

        # Variables
        self.playlist = []
        self.current_song_index = 0
        self.is_paused = False
        self.selected_folder = ""

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        # Dropdown menu for songs
        self.song_var = tk.StringVar(value="Select a song")
        self.song_menu = tk.OptionMenu(self.root, self.song_var, "Select a song")
        self.song_menu.config(bg='black', fg='white', font=('Helvetica', 12))
        self.song_menu.pack(pady=20)

        # Control buttons
        control_frame = tk.Frame(self.root, bg='gray')
        control_frame.pack()

        self.play_button = tk.Button(control_frame, text="Play", command=self.play_pause, bg='black', fg='white', font=('Helvetica', 12))
        self.play_button.grid(row=0, column=0, padx=10)

        self.stop_button = tk.Button(control_frame, text="Stop", command=self.stop_song, bg='black', fg='white', font=('Helvetica', 12))
        self.stop_button.grid(row=0, column=1, padx=10)

        self.load_button = tk.Button(control_frame, text="Load Folder", command=self.load_folder, bg='black', fg='white', font=('Helvetica', 12))
        self.load_button.grid(row=0, column=2, padx=10)

        # Volume control
        self.volume_scale = tk.Scale(self.root, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.01, command=self.set_volume, bg='gray', fg='white', font=('Helvetica', 12))
        self.volume_scale.set(0.5)
        self.volume_scale.pack(pady=20)

    def update_song_menu(self):
        menu = self.song_menu['menu']
        menu.delete(0, 'end')
        for song in self.playlist:
            menu.add_command(label=song, command=tk._setit(self.song_var, song))
        if self.playlist:
            self.song_var.set(self.playlist[0])

    def load_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.playlist = [f for f in os.listdir(folder_path) if f.endswith(('.mp3', '.mp4'))]
            if not self.playlist:
                messagebox.showinfo("No Songs", "No MP3 or MP4 files found in the selected folder.")
                return
            self.selected_folder = folder_path
            self.current_song_index = 0
            self.update_song_menu()
            self.stop_song()

    def play_selected_song(self, *args):
        self.play_song(self.song_var.get())

    def play_song(self, song):
        if song and self.selected_folder:
            song_path = os.path.join(self.selected_folder, song)
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.is_paused = False
            self.play_button.config(text="Pause")

    def play_pause(self):
        if pygame.mixer.music.get_busy():
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.play_button.config(text="Pause")
            else:
                pygame.mixer.music.pause()
                self.play_button.config(text="Play")
            self.is_paused = not self.is_paused
        else:
            self.play_song(self.song_var.get())

    def stop_song(self):
        pygame.mixer.music.stop()
        self.play_button.config(text="Play")
        self.is_paused = False

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaPlayer(root)
    root.mainloop()
