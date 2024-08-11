import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar
import os
import subprocess
import threading

class ScriptManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Script Manager")

        # Initialize variables
        self.script_folder = ""
        self.processes = {}
        self.script_list = []

        # Create and place widgets
        tk.Button(root, text="Select Folder", command=self.select_folder).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(root, text="Run Script", command=self.run_script).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(root, text="Stop Script", command=self.stop_script).grid(row=2, column=0, padx=10, pady=10)

        # Listbox with scrollbar for listing scripts
        self.script_listbox = Listbox(root, selectmode=tk.SINGLE, height=15, width=50)
        self.script_listbox.grid(row=0, column=1, rowspan=3, padx=10, pady=10)
        
        scrollbar = Scrollbar(root)
        scrollbar.grid(row=0, column=2, rowspan=3, sticky='ns')
        self.script_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.script_listbox.yview)

    def select_folder(self):
        """Allow the user to select a folder and list all Python scripts."""
        self.script_folder = filedialog.askdirectory()
        if not self.script_folder:
            return
        
        self.script_listbox.delete(0, tk.END)
        self.script_list = [f for f in os.listdir(self.script_folder) if f.endswith(".py")]
        
        for script in self.script_list:
            self.script_listbox.insert(tk.END, script)

    def run_script(self):
        """Run the selected script in a new terminal window."""
        selected_index = self.script_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "No script selected.")
            return
        
        script_name = self.script_list[selected_index[0]]
        script_path = os.path.join(self.script_folder, script_name)

        if script_name in self.processes:
            messagebox.showwarning("Warning", f"{script_name} is already running.")
            return

        def target():
            # Ensure the path is correctly formatted for the command
            script_path_quoted = f'"{os.path.normpath(script_path)}"'

            # Determine the command to open a new terminal and run the script
            if os.name == 'nt':  # Windows
                process = subprocess.Popen(['start', 'cmd', '/k', f'python {script_path_quoted}'], shell=True)
            else:  # MacOS/Linux
                process = subprocess.Popen(['gnome-terminal', '--', 'python3', script_path])

            self.processes[script_name] = process
            process.wait()
            del self.processes[script_name]

        thread = threading.Thread(target=target)
        thread.start()

    def stop_script(self):
        """Stop the selected script."""
        selected_index = self.script_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "No script selected.")
            return

        script_name = self.script_list[selected_index[0]]

        if script_name not in self.processes:
            messagebox.showwarning("Warning", f"{script_name} is not running.")
            return

        process = self.processes[script_name]
        process.terminate()
        del self.processes[script_name]
        messagebox.showinfo("Info", f"{script_name} has been stopped.")

# Create main window
def main():
    root = tk.Tk()
    app = ScriptManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
