import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import glob
import platform
import subprocess

def find_jpg_files(start_dir):
    """Find all .jpg files starting from the given directory."""
    jpg_files = []
    for root, _, files in os.walk(start_dir):
        for file in files:
            if file.lower().endswith('.jpg'):
                jpg_files.append(os.path.join(root, file))
    return jpg_files

def open_image(image_path):
    """Open the selected image with the default viewer."""
    if platform.system() == "Windows":
        os.startfile(image_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", image_path])
    else:  # Linux
        subprocess.run(["xdg-open", image_path])

def on_image_select(event):
    """Handle the image selection from the listbox."""
    selected_index = listbox.curselection()
    if selected_index:
        image_path = jpg_files[selected_index[0]]
        open_image(image_path)

def load_images():
    """Load and display thumbnails of .jpg files."""
    global jpg_files
    jpg_files = find_jpg_files(start_dir_entry.get())
    listbox.delete(0, tk.END)
    for file in jpg_files:
        try:
            img = Image.open(file)
            img.thumbnail((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            listbox.insert(tk.END, file)
            listbox.itemconfig(tk.END, {'image': img_tk})
        except Exception as e:
            print(f"Could not open image {file}: {e}")

def choose_directory():
    """Open a dialog to choose the directory."""
    folder = filedialog.askdirectory()
    if folder:
        start_dir_entry.delete(0, tk.END)
        start_dir_entry.insert(0, folder)
        load_images()

# Create main window
root = tk.Tk()
root.title("JPG File Locator")

# Directory selection
tk.Label(root, text="Start Directory").grid(row=0, column=0)
start_dir_entry = tk.Entry(root, width=50)
start_dir_entry.grid(row=0, column=1)
tk.Button(root, text="Browse", command=choose_directory).grid(row=0, column=2)

# Listbox with images
listbox = tk.Listbox(root, width=80, height=20)
listbox.grid(row=1, column=0, columnspan=3)
listbox.bind("<Double-1>", on_image_select)

root.mainloop()
