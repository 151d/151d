import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def select_save_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_save_directory.delete(0, tk.END)
        entry_save_directory.insert(0, directory)

def convert_to_jpg():
    file_path = entry_file_path.get()
    save_directory = entry_save_directory.get()
    if not file_path:
        messagebox.showerror("Error", "Please select an image file.")
        return
    if not save_directory:
        messagebox.showerror("Error", "Please select a save directory.")
        return
    
    try:
        img = Image.open(file_path)
        rgb_img = img.convert('RGB')
        
        # Create the output path
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(save_directory, base_name + ".jpg")
        
        rgb_img.save(output_path, "JPEG")
        
        messagebox.showinfo("Success", f"Image successfully converted and saved to {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the main window
root = tk.Tk()
root.title("Image to JPG Converter")

# Create and place widgets
label_file_path = tk.Label(root, text="Select an image file:")
label_file_path.pack(pady=5)

entry_file_path = tk.Entry(root, width=50)
entry_file_path.pack(pady=5)

button_browse = tk.Button(root, text="Browse", command=browse_file)
button_browse.pack(pady=5)

label_save_directory = tk.Label(root, text="Select save directory:")
label_save_directory.pack(pady=5)

entry_save_directory = tk.Entry(root, width=50)
entry_save_directory.pack(pady=5)

button_save_directory = tk.Button(root, text="Select Directory", command=select_save_directory)
button_save_directory.pack(pady=5)

button_convert = tk.Button(root, text="Convert to JPG", command=convert_to_jpg)
button_convert.pack(pady=20)

# Run the application
root.mainloop()
