import tkinter as tk
from pygame import mixer

# Initialize the mixer
mixer.init()

# Load your sounds (replace with your actual sound files)
sounds = [
    'sound1.mp4', 'sound2.mp3', 'sound3.mp3', 'sound4.mp3', 'sound5.mp3',
    'sound6.mp3', 'sound7.mp3', 'sound8.mp3', 'sound9.mp3', 'sound10.mp3',
    'sound11.mp3', 'sound12.mp3', 'sound13.mp3', 'sound14.mp3', 'sound15.mp3',
    'sound16.mp3', 'sound17.mp3', 'sound18.mp3', 'sound19.mp3', 'sound20.mp3'
]

# Function to play sound
def play_sound(index):
    mixer.music.load(sounds[index])
    mixer.music.play()

# Create the main window
root = tk.Tk()
root.title("Music Board")

# Create and place buttons
for i in range(20):
    btn = tk.Button(root, text=f"Sound {i+1}", command=lambda i=i: play_sound(i), width=10, height=3)
    btn.grid(row=i//5, column=i%5, padx=5, pady=5)

# Run the application
root.mainloop()
