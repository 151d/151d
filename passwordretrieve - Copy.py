import os
import sqlite3
import json
import base64
import shutil
from Cryptodome.Cipher import AES
import win32crypt
import sys
import win32cred
import tkinter as tk
from tkinter import ttk

# Function to get Chrome database path
def get_chrome_db():
    path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
    temp_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data.temp'
    if os.path.exists(temp_path):
        os.remove(temp_path)
    shutil.copy2(path, temp_path)
    return temp_path

# Function to get secret key for Chrome
def get_secret_key():
    local_state_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Local State'
    with open(local_state_path, 'r', encoding='utf-8') as f:
        local_state_data = json.load(f)
    encrypted_key = base64.b64decode(local_state_data['os_crypt']['encrypted_key'])
    encrypted_key = encrypted_key[5:]  # Remove DPAPI prefix
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

# Function to decrypt Chrome passwords
def decrypt_password(buff, secret_key):
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(secret_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)[:-16].decode()
    return decrypted_pass

# Function to get Chrome passwords
def get_chrome_passwords():
    db_path = get_chrome_db()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    encrypted_key = get_secret_key()
    passwords = []

    for r in cursor.fetchall():
        url = r[0]
        username = r[1]
        encrypted_password = r[2]
        try:
            decrypted_password = decrypt_password(encrypted_password, encrypted_key)
        except Exception:
            continue
        passwords.append((url, username, decrypted_password))
    
    conn.close()
    return passwords

# Function to get Windows credentials
def get_windows_credentials():
    creds = []
    creds_data = win32cred.CredEnumerate(None, 0)
    for cred in creds_data:
        target = cred['TargetName']
        username = cred['UserName']
        try:
            password_blob = win32cred.CredRead(target, cred['Type'])
            password = password_blob['CredentialBlob'].decode('utf-16-le')
        except UnicodeDecodeError:
            password = password_blob['CredentialBlob'].decode('utf-8', errors='ignore')
        creds.append((target, username, password))
    return creds

# Function to display passwords in a Tkinter window
def display_passwords(passwords):
    root = tk.Tk()
    root.title("Saved Passwords")

    tree = ttk.Treeview(root)
    tree["columns"] = ("Source", "URL", "Username", "Password")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Source", anchor=tk.W, width=100)
    tree.column("URL", anchor=tk.W, width=400)
    tree.column("Username", anchor=tk.W, width=150)
    tree.column("Password", anchor=tk.W, width=150)

    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Source", text="Source", anchor=tk.W)
    tree.heading("URL", text="URL", anchor=tk.W)
    tree.heading("Username", text="Username", anchor=tk.W)
    tree.heading("Password", text="Password", anchor=tk.W)

    for p in passwords:
        tree.insert("", tk.END, values=p)

    tree.pack(expand=True, fill='both')
    root.mainloop()

# Main function
def main():
    if sys.platform != 'win32':
        print("This script only works on Windows.")
        sys.exit(1)

    all_passwords = []

    print("Retrieving Chrome passwords...")
    chrome_passwords = get_chrome_passwords()
    all_passwords.extend([('Chrome', *p) for p in chrome_passwords])

    print("Retrieving Windows credentials...")
    windows_passwords = get_windows_credentials()
    all_passwords.extend([('Windows', *p) for p in windows_passwords])

    if all_passwords:
        display_passwords(all_passwords)
    else:
        print("No passwords found.")

if __name__ == "__main__":
    main()
