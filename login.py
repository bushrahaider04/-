


# login.py




import sqlite3
import tkinter as tk
from tkinter import messagebox

DATABASE = "users.db"
SHIFT = 3


# -------------------------------------------------
# DATABASE SETUP
# -------------------------------------------------

def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        """
    )

    conn.commit()
    conn.close()


# -------------------------------------------------
# CAESAR ENCRYPTION
# -------------------------------------------------

def caesar_encrypt(text, shift=SHIFT):
    result = ""

    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char

    return result


# -------------------------------------------------
# USER REGISTRATION
# -------------------------------------------------

def register_user(username, password):
    encrypted_password = caesar_encrypt(password)

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, encrypted_password)
        )

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:
        return False


# -------------------------------------------------
# LOGIN VERIFICATION
# -------------------------------------------------

def verify_user(username, password):
    encrypted_password = caesar_encrypt(password)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, encrypted_password)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


# -------------------------------------------------
# LOGIN WINDOW
# -------------------------------------------------

def launch_login_window(on_success):

    create_database()

    window = tk.Toplevel()
    window.title("Secure Login")
    window.geometry("350x250")
    window.resizable(False, False)

    tk.Label(window, text="Username").pack(pady=5)
    username_entry = tk.Entry(window, width=30)
    username_entry.pack()

    tk.Label(window, text="Password").pack(pady=5)
    password_entry = tk.Entry(window, show="*", width=30)
    password_entry.pack()

    def login_action():
        username = username_entry.get()
        password = password_entry.get()

        if verify_user(username, password):
            messagebox.showinfo("Success", "Login Successful")
            window.destroy()
            on_success()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    def register_action():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Fields cannot be empty")
            return

        if register_user(username, password):
            messagebox.showinfo("Success", "Registration Successful")
        else:
            messagebox.showerror("Error", "Username already exists")

    tk.Button(window, text="Login", width=15, command=login_action).pack(pady=10)
    tk.Button(window, text="Register", width=15, command=register_action).pack()

    return window






