import os
import subprocess
import tkinter as tk
from tkinter import filedialog, Listbox, messagebox
import pygame

def show_intro():
    intro_window = tk.Toplevel(root)
    intro_window.title("Welcome")
    intro_window.geometry("400x200")

    intro_label = tk.Label(intro_window, text="Welcome to Python Script Organizer!", font=("Arial", 14))
    intro_label.pack(pady=20)

    details = """This tool allows you to:
    1. Select a folder containing your Python scripts.
    2. View and organize all Python (.py) files in that folder.
    3. Run any selected Python script with a single click.
    4. Remove any selected Python script from the folder.

    Enjoy managing your scripts more efficiently!"""
    details_label = tk.Label(intro_window, text=details, justify="left", wraplength=350)
    details_label.pack(pady=10)

    close_button = tk.Button(intro_window, text="Get Started", command=lambda: close_intro(intro_window))
    close_button.pack(pady=20)

def close_intro(window):
    play_sound()
    window.destroy()

def play_sound():
    if os.path.exists('button_click.wav'):
        pygame.mixer.Sound('button_click.wav').play()
    else:
        print("Sound file not found.")

def select_folder():
    play_sound()
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_label.config(text=folder_path)
        populate_listbox(folder_path)

def populate_listbox(folder_path):
    listbox.delete(0, tk.END)
    python_files = [f for f in os.listdir(folder_path) if f.endswith('.py')]
    if python_files:
        for file_name in python_files:
            listbox.insert(tk.END, file_name)
    else:
        messagebox.showinfo("Info", "No Python files found in the selected folder.")

def run_script():
    play_sound()
    selected_script = listbox.get(tk.ACTIVE)
    if selected_script:
        script_path = os.path.join(folder_label.cget("text"), selected_script)
        try:
            subprocess.run(['python', script_path], check=True)
            messagebox.showinfo("Success", f"'{selected_script}' ran successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error running '{selected_script}': {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
    else:
        messagebox.showwarning("Warning", "No script selected.")

def remove_script():
    play_sound()
    selected_script = listbox.get(tk.ACTIVE)
    if selected_script:
        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{selected_script}'?")
        if confirm:
            script_path = os.path.join(folder_label.cget("text"), selected_script)
            try:
                os.remove(script_path)
                populate_listbox(folder_label.cget("text"))
                messagebox.showinfo("Success", f"'{selected_script}' was removed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error removing '{selected_script}': {e}")
    else:
        messagebox.showwarning("Warning", "No script selected.")

# Initialize pygame for sound
pygame.mixer.init()

# Set up the main application window
root = tk.Tk()
root.title("Python Script Organizer")

# Show intro window
show_intro()

# Folder selection button
folder_button = tk.Button(root, text="Select Folder", command=select_folder)
folder_button.pack(pady=10)

# Label to display selected folder
folder_label = tk.Label(root, text="No folder selected")
folder_label.pack(pady=5)

# Listbox to display Python scripts
listbox = Listbox(root, width=50)
listbox.pack(pady=10)

# Run button to execute the selected script
run_button = tk.Button(root, text="Run Selected Script", command=run_script)
run_button.pack(pady=5)

# Remove button to delete the selected script
remove_button = tk.Button(root, text="Remove Selected Script", command=remove_script)
remove_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
