import time
from datetime import datetime
import os
import win32gui

# Path to the log file in the Documents folder
log_file_path = os.path.join(os.environ['USERPROFILE'], 'Documents', 'activity_log.txt')

def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwnd)

def log_activity():
    with open(log_file_path, 'a', encoding='utf-8') as f:
        while True:
            active_window = get_active_window_title()
            if active_window:
                f.write(f"{datetime.now()} - {active_window}\n")
            time.sleep(5)  # Log every 5 seconds

if __name__ == "__main__":
    log_activity()
