import time
from datetime import datetime
import os
import threading
import tkinter as tk
from tkinter import messagebox
import win32gui
import win32api

# Path to the log file in the Documents folder
log_file_path = os.path.join(os.environ['USERPROFILE'], 'Documents', 'combined_log.txt')

class ActivityLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Activity Logger")
        self.logging = False
        self.logging_keystrokes = False

        # Create GUI elements
        self.start_button = tk.Button(root, text="Start Logging", command=self.start_logging)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Logging", command=self.stop_logging, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.open_file_button = tk.Button(root, text="Open Log File", command=self.open_log_file)
        self.open_file_button.pack(pady=10)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(pady=10)

        # Bind hotkeys
        self.root.bind('<Control-h>', self.open_log_file)  # Use Control-h as a hotkey

    def get_active_window_title(self):
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)

    def log_activity(self):
        with open(log_file_path, 'a', encoding='utf-8') as f:
            last_active_window = ""
            while self.logging:
                active_window = self.get_active_window_title()
                if active_window != last_active_window:
                    last_active_window = active_window
                    f.write(f"{datetime.now()} - Active Window: {active_window}\n")
                time.sleep(5)  # Log every 5 seconds

    def log_keystrokes(self):
        def on_key_event(key_str):
            with open(log_file_path, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now()} - Keystroke: {key_str}\n")

        while self.logging_keystrokes:
            for key in range(0, 256):
                if win32api.GetAsyncKeyState(key) & 0x8000:
                    key_str = self.get_key_name(key)
                    on_key_event(key_str)
            time.sleep(0.1)  # Check every 100 milliseconds

    def get_key_name(self, key_code):
        try:
            return chr(key_code)
        except ValueError:
            return f"Key code {key_code}"

    def start_logging(self):
        self.logging = True
        self.logging_keystrokes = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Start the logging threads
        self.logging_thread = threading.Thread(target=self.log_activity, daemon=True)
        self.logging_thread.start()

        self.keystroke_thread = threading.Thread(target=self.log_keystrokes, daemon=True)
        self.keystroke_thread.start()

    def stop_logging(self):
        self.logging = False
        self.logging_keystrokes = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # Wait for the logging threads to finish
        self.logging_thread.join()
        self.keystroke_thread.join()

    def open_log_file(self, event=None):
        # Open the log file using the default text editor
        if os.path.exists(log_file_path):
            os.startfile(log_file_path)
        else:
            messagebox.showerror("Error", "Log file does not exist.")

# Create and run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = ActivityLoggerApp(root)
    root.mainloop()
