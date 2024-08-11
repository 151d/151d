from pynput import keyboard
import subprocess
import threading

def run_background_task():
    # Replace 'your_background_task.py' with the actual script or command you want to run
    subprocess.Popen(['python', 'your_background_task.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)

def on_press(key):
    try:
        # Check if the key is a character key and if it's part of a username/password input
        if key.char and key.char.isalnum():
            print(f"Key pressed: {key.char}")
            # Here you can add the logic to activate your script
            # Start the background task in a new thread
            threading.Thread(target=run_background_task).start()
    except AttributeError:
        pass

def on_release(key):
    # Stop the listener if a specific key is released, for example, the escape key
    if key == keyboard.Key.esc:
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
