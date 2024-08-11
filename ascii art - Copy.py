import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import colorchooser
import pyfiglet
import requests

# Fetch the list of fonts from the pyfiglet GitHub repository
def fetch_fonts():
    url = "https://raw.githubusercontent.com/pwaller/pyfiglet/master/pyfiglet/fonts.md"
    response = requests.get(url)
    fonts = []
    if response.status_code == 200:
        lines = response.text.split('\n')
        for line in lines:
            if line.startswith('- '):
                fonts.append(line[2:])
    return fonts

# Generate ASCII art
def generate_ascii_art(text, font='standard'):
    try:
        ascii_art = pyfiglet.figlet_format(text, font=font, width=100)
        return ascii_art
    except Exception as e:
        return str(e)

# Convert button click handler
def convert_text_to_ascii():
    text = text_entry.get()
    font = font_combobox.get()
    color = color_var.get()
    ascii_art = generate_ascii_art(text, font)
    
    result_display.configure(state='normal')
    result_display.delete(1.0, tk.END)
    result_display.insert(tk.INSERT, ascii_art)
    result_display.configure(state='disabled')
    
    result_display.tag_configure("colored", foreground=color)
    result_display.tag_add("colored", "1.0", "end")

# Color picker handler
def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")[1]
    if color_code:
        color_var.set(color_code)
        color_button.configure(bg=color_code)

# Fetch fonts list
fonts = fetch_fonts()

# GUI setup
root = tk.Tk()
root.title("ASCII Art Generator")

# Text entry
tk.Label(root, text="Enter Text:").grid(row=0, column=0, padx=10, pady=10)
text_entry = tk.Entry(root, width=50)
text_entry.grid(row=0, column=1, padx=10, pady=10)

# Font selection
tk.Label(root, text="Select Font:").grid(row=1, column=0, padx=10, pady=10)
font_combobox = ttk.Combobox(root, values=fonts, width=47)
font_combobox.set("standard")
font_combobox.grid(row=1, column=1, padx=10, pady=10)

# Color selection
tk.Label(root, text="Select Color:").grid(row=2, column=0, padx=10, pady=10)
color_var = tk.StringVar(value="#000000")
color_button = tk.Button(root, text="Choose Color", command=choose_color, bg=color_var.get())
color_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Convert button
convert_button = tk.Button(root, text="Convert", command=convert_text_to_ascii)
convert_button.grid(row=3, column=0, columnspan=2, pady=10)

# Result display
result_display = scrolledtext.ScrolledText(root, width=80, height=20, state='disabled')
result_display.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
