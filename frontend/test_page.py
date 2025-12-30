import tkinter as tk
from tkinter import messagebox
import requests

# Point this to your backend
API_URL = "http://localhost:8000/api/test-hardware"

def send_test_signal():
    try:
        # Get data from input boxes
        elem = entry_elem.get()
        val = int(entry_val.get())
        
        # Send to Backend
        payload = {"element": elem, "value": val}
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                lbl_status.config(text=f" {data['message']}", fg="green")
            else:
                lbl_status.config(text=f" {data.get('error')}", fg="red")
        else:
            lbl_status.config(text=" Server Error", fg="red")
            
    except ValueError:
        messagebox.showerror("Error", "Value must be a number!")
    except Exception as e:
        messagebox.showerror("Connection Error", f"Is Backend running?\n{e}")

# Build the Window
root = tk.Tk()
root.title("Hardware Link Test")
root.geometry("400x300")

tk.Label(root, text="Element (e.g., Fe):", font=("Arial", 12)).pack(pady=5)
entry_elem = tk.Entry(root, font=("Arial", 12))
entry_elem.insert(0, "Fe")
entry_elem.pack()

tk.Label(root, text="Value (0-64):", font=("Arial", 12)).pack(pady=5)
entry_val = tk.Entry(root, font=("Arial", 12))
entry_val.insert(0, "77")
entry_val.pack()

btn = tk.Button(root, text="SEND TO HARDWARE", command=send_test_signal, 
                bg="#5c9bd5", fg="white", font=("Arial", 12, "bold"), height=2)
btn.pack(pady=20)

lbl_status = tk.Label(root, text="Ready...", font=("Arial", 10))
lbl_status.pack()

root.mainloop()