import time
import tkinter as tk
from tkinter import ttk
import win32gui
import win32con
import win32process
import win32api

class TransparencyController(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Transparency Controller")
        self.geometry("400x300")

        self.label = tk.Label(self, text="Select Window:")
        self.label.pack(pady=5)

        self.window_list = self.get_window_list()
        self.window_var = tk.StringVar(self)
        self.window_var.set(self.window_list[0] if self.window_list else "No windows found")
        self.window_menu = ttk.Combobox(self, textvariable=self.window_var, values=self.window_list)
        self.window_menu.pack(pady=5)

        self.slider_label = tk.Label(self, text="Transparency:")
        self.slider_label.pack(pady=5)

        self.transparency_slider = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_transparency)
        self.transparency_slider.set(100)
        self.transparency_slider.pack(pady=5)

        self.close_button = tk.Button(self, text="Close Window", command=self.close_window)
        self.close_button.pack(pady=10)

        self.startup_animation()

    def get_window_list(self):
        windows = []
        def enum_window_proc(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                windows.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_window_proc, None)
        return [win32gui.GetWindowText(hwnd) for hwnd, title in windows if title]

    def get_hwnd_by_title(self, title):
        windows = []
        def enum_window_proc(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                windows.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_window_proc, None)
        for hwnd, window_title in windows:
            if window_title == title:
                return hwnd
        return None

    def update_transparency(self, value):
        selected_window = self.window_var.get()
        transparency_value = int(value)
        hwnd = self.get_hwnd_by_title(selected_window)
        if hwnd:
            print(f"Updating transparency for window: {selected_window} (HWND: {hwnd})")
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
            win32gui.SetLayeredWindowAttributes(hwnd, 0, int(transparency_value * 2.55), win32con.LWA_ALPHA)
        else:
            print(f"Window not found: {selected_window}")

    def close_window(self):
        selected_window = self.window_var.get()
        hwnd = self.get_hwnd_by_title(selected_window)
        if hwnd:
            # Reset transparency to 100%
            print(f"Resetting transparency for window: {selected_window} (HWND: {hwnd})")
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
            win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)

            # Terminate the process
            print(f"Terminating process for window: {selected_window} (HWND: {hwnd})")
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, pid)
                win32api.TerminateProcess(handle, 0)
                win32api.CloseHandle(handle)
            except Exception as e:
                print(f"Failed to terminate process: {e}")
        else:
            print(f"Window not found: {selected_window}")

    def startup_animation(self):
        animation_window = tk.Toplevel(self)
        animation_window.geometry("400x200")
        animation_window.overrideredirect(1)

        label = tk.Label(animation_window, text="Starting...", font=("Helvetica", 20))
        label.pack(expand=True)

        for i in range(101):
            label.config(text=f"Starting... {i}%")
            self.update_idletasks()
            time.sleep(0.02)

        animation_window.destroy()

if __name__ == "__main__":
    app = TransparencyController()
    app.mainloop()
