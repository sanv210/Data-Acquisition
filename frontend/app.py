import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import pages
from pages.analytical_condition import AnalyticalConditionPage


class AnalyticalInformationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analytical Information")
        self.root.geometry("800x600")
        self.root.configure(bg='#d4d0c8')
        
        # Set the window icon (optional, can be added later)
        # self.root.iconbitmap('assets/icon.ico')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#d4d0c8')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title Label
        title_label = tk.Label(
            main_frame,
            text="Analytical Group Information",
            font=('Arial', 10),
            bg='#d4d0c8',
            anchor='w'
        )
        title_label.pack(fill=tk.X, pady=(0, 5))
        
        # Content frame with border
        content_frame = tk.Frame(main_frame, bg='white', relief=tk.SUNKEN, bd=2)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for list
        left_panel = tk.Frame(content_frame, bg='#d4d0c8', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        
        # Label for Analytical Group
        list_label = tk.Label(
            left_panel,
            text="Analytical Group",
            font=('Arial', 9),
            bg='#d4d0c8'
        )
        list_label.pack(pady=(5, 2))
        
        # Listbox with scrollbar
        list_frame = tk.Frame(left_panel)
        list_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.analytical_listbox = tk.Listbox(
            list_frame,
            font=('Arial', 9),
            bg='white',
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            width=25,
            height=20
        )
        self.analytical_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.analytical_listbox.yview)
        
        # Populate the listbox with sample data
        analytical_groups = [
            "LAS 2023",
            "SS 2023",
            "LA 2021",
            "SS - 2022",
            "FERR 2022",
            "TOLL STEEL2021",
            "FERR 2020",
            "SS 2021",
            "LA 2021 S",
            "GLOBAL CAL",
            "LA 2020",
            "LA-WITH HI MN",
            "SS WITH HI MN",
            "Cast",
            "LOW-ALLOY-HS",
            "NI 2017",
            "INCONEL 17",
            "MONEL 17",
            "TEST GROUP",
            "LA 2021 WITH CA",
            "TEST LAS",
            "26-11-22",
            "FERR 2023",
            "GHHaj"
        ]
        
        for group in analytical_groups:
            self.analytical_listbox.insert(tk.END, group)
        
        # Select the first item by default
        self.analytical_listbox.selection_set(0)
        
        # Buttons panel
        button_panel = tk.Frame(left_panel, bg='#d4d0c8')
        button_panel.pack(pady=10, padx=10)
        
        # Button configuration
        button_config = {
            'width': 12,
            'font': ('Arial', 9),
            'bg': '#d4d0c8',
            'relief': tk.RAISED,
            'bd': 2
        }
        
        # 1.Select button
        select_btn = tk.Button(
            button_panel,
            text="1.Select",
            command=self.on_next_clicked,
            **button_config
        )
        select_btn.grid(row=0, column=0, pady=3, sticky='ew')
        
        # 2.Detail button
        detail_btn = tk.Button(
            button_panel,
            text="2.Detail",
            command=self.on_detail_clicked,
            **button_config
        )
        detail_btn.grid(row=1, column=0, pady=3, sticky='ew')
        
        # 9.Arrange button
        arrange_btn = tk.Button(
            button_panel,
            text="9.Arrange",
            command=self.on_arrange_clicked,
            **button_config
        )
        arrange_btn.grid(row=2, column=0, pady=3, sticky='ew')
        
        # 6.New button
        new_btn = tk.Button(
            button_panel,
            text="6.New",
            command=self.on_new_clicked,
            **button_config
        )
        new_btn.grid(row=3, column=0, pady=3, sticky='ew')
        
        # 8.Delete button
        delete_btn = tk.Button(
            button_panel,
            text="8.Delete",
            command=self.on_delete_clicked,
            **button_config
        )
        delete_btn.grid(row=4, column=0, pady=3, sticky='ew')
        
        # 9.WC Cost Copy button
        wc_cost_btn = tk.Button(
            button_panel,
            text="9.WC Cost Copy",
            command=self.on_wc_cost_copy_clicked,
            **button_config
        )
        wc_cost_btn.grid(row=5, column=0, pady=3, sticky='ew')
        
        # Right panel (empty for now, can be used for details)
        self.right_panel = tk.Frame(content_frame, bg='#d4d0c8')
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def get_selected_group(self):
        """Get the currently selected analytical group"""
        selection = self.analytical_listbox.curselection()
        if selection:
            return self.analytical_listbox.get(selection[0])
        return None
    
    def on_next_clicked(self):
        """Handler for Select button - This will navigate to the next page"""
        selected = self.get_selected_group()
        if selected:
            print(f"Selected group: {selected}")
            for widget in self.right_panel.winfo_children():
                widget.destroy()
            
            # Load AnalyticalConditionPage inside right panel
            AnalyticalConditionPage(self.right_panel, selected, self)
            # Navigate to Analytical Condition page
            # AnalyticalConditionPage(self.root, selected, self)
        else:
            messagebox.showwarning("Warning", "Please select an analytical group first")
    
    def on_detail_clicked(self):
        """Handler for Detail button"""
        selected = self.get_selected_group()
        if selected:
            messagebox.showinfo("Detail", f"Showing details for: {selected}")
        else:
            messagebox.showwarning("Warning", "Please select an analytical group first")
    
    def on_arrange_clicked(self):
        """Handler for Arrange button"""
        messagebox.showinfo("Arrange", "Arrange functionality")
    
    def on_new_clicked(self):
        """Handler for New button"""
        messagebox.showinfo("New", "Create new analytical group")
    
    def on_delete_clicked(self):
        """Handler for Delete button"""
        selected = self.get_selected_group()
        if selected:
            confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete '{selected}'?")
            if confirm:
                selection = self.analytical_listbox.curselection()
                if selection:
                    self.analytical_listbox.delete(selection[0])
        else:
            messagebox.showwarning("Warning", "Please select an analytical group first")
    
    def on_wc_cost_copy_clicked(self):
        """Handler for WC Cost Copy button"""
        selected = self.get_selected_group()
        if selected:
            messagebox.showinfo("WC Cost Copy", f"Copying WC Cost for: {selected}")
        else:
            messagebox.showwarning("Warning", "Please select an analytical group first")


def main():
    root = tk.Tk()
    app = AnalyticalInformationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
