import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import itertools
import gzip
import threading
import os

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")

        # Initialize variables
        self.is_generating = False
        self.thread = None
        self.output_file = None

        # Create and place widgets
        tk.Label(root, text="Select Password Length (1-10):").grid(row=0, column=0, padx=10, pady=10)
        
        self.length_var = tk.StringVar(value="1")
        length_entry = ttk.Combobox(root, textvariable=self.length_var, values=[str(i) for i in range(1, 11)])
        length_entry.grid(row=0, column=1, padx=10, pady=10)
        length_entry.set("1")

        self.start_button = tk.Button(root, text="Start Generation", command=self.start_generation)
        self.start_button.grid(row=1, column=0, padx=10, pady=10)
        
        self.stop_button = tk.Button(root, text="Stop Generation", command=self.stop_generation, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1, padx=10, pady=10)

        self.save_button = tk.Button(root, text="Save File", command=self.save_file, state=tk.DISABLED)
        self.save_button.grid(row=2, column=0, columnspan=2, pady=20)

    def generate_passwords(self, length, characters):
        """Generate all possible passwords of a given length from the provided characters."""
        return itertools.product(characters, repeat=length)

    def save_passwords_to_file(self, passwords, filename):
        """Save the generated passwords to a .txt.gz file."""
        with gzip.open(filename, 'wt', encoding='utf-8') as f:
            for password in passwords:
                f.write(''.join(password) + '\n')

    def start_generation(self):
        """Start the password generation in a separate thread."""
        if self.is_generating:
            messagebox.showwarning("Warning", "Generation is already in progress.")
            return

        self.output_file = filedialog.asksaveasfilename(defaultextension=".txt.gz", filetypes=[("Gzip files", "*.gz"), ("Text files", "*.txt")])
        if not self.output_file:
            return

        self.is_generating = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)

        length = int(self.length_var.get())
        characters = 'abcdefghijklmnopqrstuvwxyz0123456789'

        self.thread = threading.Thread(target=self.generate_and_save, args=(length, characters))
        self.thread.start()

    def stop_generation(self):
        """Stop the password generation."""
        if self.is_generating:
            self.is_generating = False
            self.thread.join()
            messagebox.showinfo("Stopped", "Password generation stopped.")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.save_button.config(state=tk.NORMAL)

    def generate_and_save(self, length, characters):
        """Generate passwords and save them to a file."""
        try:
            print("Generating passwords...")
            passwords = self.generate_passwords(length, characters)
            with gzip.open(self.output_file, 'wt', encoding='utf-8') as f:
                for password in passwords:
                    if not self.is_generating:
                        break
                    f.write(''.join(password) + '\n')
            print("Done.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.is_generating = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.save_button.config(state=tk.NORMAL)

    def save_file(self):
        """Handle the save file action."""
        if not self.output_file or not os.path.exists(self.output_file):
            messagebox.showwarning("Warning", "No file to save. Please generate passwords first.")
            return

        messagebox.showinfo("Saved", f"Passwords have been saved to {self.output_file}.")

# Create main window
root = tk.Tk()
app = PasswordGeneratorApp(root)
root.mainloop()
