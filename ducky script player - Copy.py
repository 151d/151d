import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext  # Import ScrolledText here
import pyautogui
import time

class BadUSBEmulator:
    def __init__(self, root):
        self.root = root
        self.root.title("BadUSB Emulator")

        # Frame for buttons
        frame = tk.Frame(root)
        frame.pack(pady=10)

        # Open file button
        self.open_button = tk.Button(frame, text="Open Ducky Script", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=10)

        # Run script button
        self.run_button = tk.Button(frame, text="Run Script", command=self.run_script)
        self.run_button.pack(side=tk.LEFT, padx=10)

        # Stop script button
        self.stop_button = tk.Button(frame, text="Stop Script", command=self.stop_script)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        # Clear script button
        self.clear_button = tk.Button(frame, text="Clear Script", command=self.clear_script)
        self.clear_button.pack(side=tk.LEFT, padx=10)

        # Create BadUSB button
        self.create_button = tk.Button(frame, text="Create BadUSB", command=self.create_badusb)
        self.create_button.pack(side=tk.LEFT, padx=10)

        # Scrolled text widget to display the script
        self.script_display = scrolledtext.ScrolledText(root, width=80, height=20)
        self.script_display.pack(pady=10)

        # Variable to store the current file path
        self.current_file_path = None
        self.is_running = False

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                script_content = file.read()
            self.script_display.delete(1.0, tk.END)
            self.script_display.insert(tk.END, script_content)
            self.current_file_path = file_path

    def parse_ducky_script(self, ducky_script):
        commands = []
        with open(ducky_script, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("//"):
                    commands.append(line)
        return commands

    def execute_command(self, command):
        if not self.is_running:
            return
        parts = command.split()
        action = parts[0].upper()

        if action == "DELAY":
            delay_time = int(parts[1]) / 1000.0
            time.sleep(delay_time)
        elif action == "STRING":
            string = " ".join(parts[1:])
            pyautogui.typewrite(string)
        elif action == "ENTER":
            pyautogui.press('enter')
        elif action == "GUI" or action == "WINDOWS":
            pyautogui.hotkey('win', parts[1].lower())
        elif action == "SHIFT":
            pyautogui.hotkey('shift', parts[1].lower())
        elif action == "ALT":
            pyautogui.hotkey('alt', parts[1].lower())
        elif action == "CONTROL" or action == "CTRL":
            pyautogui.hotkey('ctrl', parts[1].lower())
        else:
            print(f"Unsupported command: {command}")

    def run_ducky_script(self, ducky_script):
        commands = self.parse_ducky_script(ducky_script)
        for command in commands:
            self.execute_command(command)
            if not self.is_running:
                break
            time.sleep(0.1)  # Small delay between commands to ensure proper execution

    def run_script(self):
        if self.current_file_path and not self.is_running:
            self.is_running = True
            self.run_ducky_script(self.current_file_path)
            self.is_running = False
        else:
            print("No script loaded or script already running.")

    def stop_script(self):
        self.is_running = False

    def clear_script(self):
        self.script_display.delete(1.0, tk.END)
        self.current_file_path = None

    def format_drive(self, drive_letter):
        # Warning: This is a destructive action. Use with caution.
        # On Windows, use diskpart to format the drive.
        os.system(f'diskpart /s format_script.txt')
        with open('format_script.txt', 'w') as f:
            f.write(f'select volume {drive_letter}\n')
            f.write('format fs=ntfs quick\n')
            f.write('assign\n')
            f.write('exit\n')

    def create_autorun(self, drive_letter):
        # Create an autorun.inf file on the USB drive
        autorun_content = '[autorun]\nopen=ducky.bat\n'
        autorun_path = os.path.join(drive_letter, 'autorun.inf')
        with open(autorun_path, 'w') as f:
            f.write(autorun_content)

    def create_ducky_batch(self, drive_letter):
        # Convert the Ducky script into a batch file
        if self.current_file_path:
            batch_path = os.path.join(drive_letter, 'ducky.bat')
            with open(self.current_file_path, 'r') as script_file, open(batch_path, 'w') as batch_file:
                for line in script_file:
                    if line.startswith('STRING'):
                        line = line.replace('STRING ', '')
                        batch_file.write(f'echo {line.strip()} | clip\n')
                        batch_file.write('powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait(\'^v\')"\n')
                    elif line.startswith('DELAY'):
                        delay = line.replace('DELAY ', '').strip()
                        batch_file.write(f'ping 127.0.0.1 -n {int(delay)//1000 + 1} > nul\n')
                    elif line.startswith('ENTER'):
                        batch_file.write('powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait(\'{ENTER}\')"\n')

    def create_badusb(self):
        drive_letter = filedialog.askdirectory()
        if not drive_letter:
            return
        try:
            self.format_drive(drive_letter)
            self.create_autorun(drive_letter)
            self.create_ducky_batch(drive_letter)
            messagebox.showinfo("Success", "BadUSB created successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = BadUSBEmulator(root)
    root.mainloop()
