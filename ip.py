import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from win10toast import ToastNotifier

# Function to show the notification
def show_notification(message):
    toaster = ToastNotifier()
    toaster.show_toast("Network Message", message, duration=10)

# Server function to handle incoming messages
def server_function(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    print(f"Listening for connections on port {port}...")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        message = client_socket.recv(1024).decode()
        if message:
            show_notification(message)
        client_socket.close()

# Client function to send messages
def send_message(ip, port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    client_socket.sendall(message.encode())
    client_socket.close()

# GUI function for the client
def gui_client():
    def on_send():
        ip = ip_entry.get()
        port = int(port_entry.get())
        message = message_text.get("1.0", tk.END).strip()
        send_message(ip, port, message)
        status_label.config(text="Message sent!")

    root = tk.Tk()
    root.title("Send Network Message")

    tk.Label(root, text="IP Address:").pack(pady=5)
    ip_entry = tk.Entry(root)
    ip_entry.pack(pady=5)

    tk.Label(root, text="Port:").pack(pady=5)
    port_entry = tk.Entry(root)
    port_entry.pack(pady=5)
    port_entry.insert(0, "12345")  # Default port

    tk.Label(root, text="Message:").pack(pady=5)
    message_text = tk.Text(root, height=5, width=40)
    message_text.pack(pady=5)

    send_button = tk.Button(root, text="Send Message", command=on_send)
    send_button.pack(pady=5)

    status_label = tk.Label(root, text="")
    status_label.pack(pady=5)

    root.mainloop()

# Main function to run server or client based on user input
def main():
    choice = simpledialog.askstring("Select Mode", "Type 'server' to run as server or 'client' to run as client:")

    if choice == 'server':
        port = int(simpledialog.askstring("Port", "Enter the port number to listen on:"))
        threading.Thread(target=server_function, args=(port,), daemon=True).start()
        print(f"Server started on port {port}.")
        tk.messagebox.showinfo("Server Started", f"Server is running on port {port}.")
    elif choice == 'client':
        gui_client()
    else:
        print("Invalid choice. Exiting.")
        tk.messagebox.showerror("Error", "Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
