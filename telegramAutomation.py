import requests
import tkinter as tk
from tkinter import messagebox
import datetime
import winreg as reg
import ctypes

# Telegram Bot credentials
BOT_TOKEN = "8019017261:AAEzh965mEv1CqbGGLOwnmxvqbbCiFrdUO8"
CHAT_ID = "1797951553"

MESSAGE_TEMPLATE = "Your PC has been turned on by: {} \n🕒 Timestamp: {}"

def send_notification(name):
    """Send the Telegram notification."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = MESSAGE_TEMPLATE.format(name, timestamp)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    requests.get(url, params=params)

def is_admin():
    """Check if the script is running as Administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def disable_task_manager():
    """Disable Task Manager via Registry (requires admin privileges)."""
    if not is_admin():
        print("Error: Script must be run as Administrator to disable Task Manager.")
        return

    try:
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        with reg.CreateKey(reg.HKEY_CURRENT_USER, reg_path) as key:
            reg.SetValueEx(key, "DisableTaskMgr", 0, reg.REG_DWORD, 1)
    except Exception as e:
        print(f"Error disabling Task Manager: {e}")

def enable_task_manager():
    """Re-enable Task Manager via Registry (requires admin privileges)."""
    if not is_admin():
        print("Error: Script must be run as Administrator to enable Task Manager.")
        return

    try:
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        with reg.CreateKey(reg.HKEY_CURRENT_USER, reg_path) as key:
            reg.SetValueEx(key, "DisableTaskMgr", 0, reg.REG_DWORD, 0)
    except Exception as e:
        print(f"Error enabling Task Manager: {e}")

def validate_input(event):
    """Allow only alphabetic input."""
    entry_text = entry.get()
    if not entry_text.isalpha():
        messagebox.showerror("Invalid Input", "Only letters are allowed!")
        entry.delete(0, tk.END)  # Clear entry

def get_user_name():
    """Create a fullscreen popup that locks the screen."""
    disable_task_manager()  # Disable Task Manager (if script is admin)

    global entry  
    root = tk.Tk()
    root.attributes("-fullscreen", True)  
    root.attributes("-topmost", True)  
    root.configure(bg="black")  
    root.overrideredirect(True)  

    label = tk.Label(root, text="Who turned on the PC?", font=("Arial", 24), fg="white", bg="black")
    label.pack(pady=20)

    entry = tk.Entry(root, font=("Arial", 20), width=30)
    entry.pack(pady=10)
    entry.focus_set()  
    entry.bind("<KeyRelease>", validate_input)  

    def submit_name():
        """Handle name submission and unlock screen."""
        user_name = entry.get().strip()
        if user_name.isalpha():  
            root.destroy()  
            enable_task_manager()  # Enable Task Manager (if script is admin)
            send_notification(user_name)  
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid name!")

    button = tk.Button(root, text="Submit", font=("Arial", 20), command=submit_name)
    button.pack(pady=20)

    root.mainloop()

# Run the locked window
get_user_name()
