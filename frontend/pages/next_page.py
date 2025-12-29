import tkinter as tk
from tkinter import ttk, messagebox


class NextPage:
    """
    Placeholder for the next page.
    This will be implemented once you share the design.
    """
    def __init__(self, root, selected_group=None):
        self.root = root
        self.selected_group = selected_group
        self.root.title(f"Next Page - {selected_group if selected_group else 'No Selection'}")
        self.root.geometry("800x600")
        self.root.configure(bg='#d4d0c8')
        
        self.create_widgets()
    
    def create_widgets(self):
        # Placeholder content
        label = tk.Label(
            self.root,
            text=f"Next Page\nSelected Group: {self.selected_group}",
            font=('Arial', 14),
            bg='#d4d0c8'
        )
        label.pack(expand=True)
        
        back_btn = tk.Button(
            self.root,
            text="Back",
            command=self.go_back,
            width=15,
            font=('Arial', 10)
        )
        back_btn.pack(pady=20)
    
    def go_back(self):
        """Return to the main page"""
        self.root.destroy()
        # TODO: Reopen main page