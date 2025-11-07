import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import json
from utils.data_manager import DataManager
from pages.element_information import ElementInformationPage


class AttenuatorInformationPage:
    def __init__(self, parent_frame, selected_group, parent_app=None):
        self.parent_frame = parent_frame
        self.selected_group = selected_group
        self.parent_app = parent_app
        self.data_manager = DataManager()
        
        # Store entry widgets for data collection
        self.left_att_entries = []
        self.right_att_entries = []
        
        self.create_widgets()
        self.load_saved_data()
        
    def create_widgets(self):
        # Main container frame
        main_frame = tk.Frame(self.parent_frame, bg='#d4d0c8')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title Frame
        title_frame = tk.Frame(main_frame, bg='#5c9bd5', relief=tk.RAISED, bd=2)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text=f"Attenuator Information - {self.selected_group}",
            font=('Arial', 10, 'bold'),
            bg='#5c9bd5',
            fg='white',
            anchor='w',
            padx=7,
            pady=3
        )
        title_label.pack(fill=tk.X)
        
        # Content Frame
        content_frame = tk.Frame(main_frame, bg='white', relief=tk.SUNKEN, bd=2)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        inner_frame = tk.Frame(content_frame, bg='#d4d0c8')
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tables container
        tables_frame = tk.Frame(inner_frame, bg='#d4d0c8')
        tables_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Left table data
        left_data = [
            ("FE", "273.0", "77"),
            ("C", "193.0", "49"),
            ("SI", "212.4", "41"),
            ("MN", "293.3", "40"),
            ("P", "178.3", "81"),
            ("S", "180.7", "71"),
            ("V", "311.0", "44"),
            ("CR", "267.7", "26"),
            ("CR", "298.9", "0"),
            ("MO", "202.0", "46"),
            ("MO", "277.5", "0"),
            ("NI", "231.6", "93"),
            ("NI", "227.7", "0"),
            ("AL", "394.4", "26"),
            ("CU", "224.2", "61"),
            ("TI", "337.2", "93")
        ]
        
        # Right table data - Extended with more empty rows for scrolling
        right_data = [
            ("W", "220.4", "76"),
            ("B", "182.6", "90"),
            ("NB", "319.5", "54"),
            ("CA", "396.8", "48"),
            ("CO", "258.0", "47"),
            ("SN", "189.9", "62"),
            ("N", "174.5+2", "96"),
            ("PB", "405.7", "82"),
            ("RH", "421.8", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0"),
            ("", "", "0")
        ]
        
        # Left Table
        left_table_frame = tk.Frame(tables_frame, bg='#d4d0c8')
        left_table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.create_table(left_table_frame, left_data, self.left_att_entries, scrollable=False)
        
        # Right Table with scrollbar
        right_table_frame = tk.Frame(tables_frame, bg='#d4d0c8')
        right_table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.create_table(right_table_frame, right_data, self.right_att_entries, scrollable=True)
        
        # Bottom buttons
        button_frame = tk.Frame(inner_frame, bg='#d4d0c8')
        button_frame.pack(fill=tk.X, pady=10)
        
        button_config = {
            'width': 12,
            'font': ('Arial', 9),
            'bg': '#d4d0c8',
            'relief': tk.RAISED,
            'bd': 2
        }
        
        # Left side buttons
        left_buttons = tk.Frame(button_frame, bg='#d4d0c8')
        left_buttons.pack(side=tk.LEFT)
        
        ok_btn = tk.Button(left_buttons, text="1.OK", command=self.on_ok_clicked, **button_config)
        ok_btn.pack(side=tk.LEFT, padx=3)
        
        next_btn = tk.Button(left_buttons, text="2.Next", command=self.on_next_clicked, **button_config)
        next_btn.pack(side=tk.LEFT, padx=3)
        
        pre_btn = tk.Button(left_buttons, text="3.Pre.", command=self.on_pre_clicked, **button_config)
        pre_btn.pack(side=tk.LEFT, padx=3)
        
        print_btn = tk.Button(left_buttons, text="4.Print", command=self.on_print_clicked, **button_config)
        print_btn.pack(side=tk.LEFT, padx=3)
        
        # Upload button
        upload_btn = tk.Button(left_buttons, text="Upload", command=self.on_upload_clicked, **button_config)
        upload_btn.pack(side=tk.LEFT, padx=3)
        
        # Right side button
        right_buttons = tk.Frame(button_frame, bg='#d4d0c8')
        right_buttons.pack(side=tk.RIGHT)
        
        cancel_btn = tk.Button(right_buttons, text="9.Cancel", command=self.on_cancel_clicked, **button_config)
        cancel_btn.pack(side=tk.RIGHT, padx=3)
    
    def create_table(self, parent, data, att_entries_list, scrollable=False):
        """Create a table with Ele, Ele value, and ATT columns"""
        
        if scrollable:
            # Create canvas and scrollbar for right table
            canvas = tk.Canvas(parent, bg='white', highlightthickness=1, highlightbackground='#8c8c8c')
            scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='white')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Enable mouse wheel scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            table_container = scrollable_frame
        else:
            # Non-scrollable table with border
            table_container = tk.Frame(parent, bg='white', relief=tk.SOLID, bd=1)
            table_container.pack(fill=tk.BOTH, expand=True)
        
        # Create header with better styling
        header_frame = tk.Frame(table_container, bg='#e0e0e0', relief=tk.RAISED, bd=1)
        header_frame.grid(row=0, column=0, columnspan=3, sticky='ew')
        
        tk.Label(header_frame, text="Ele", font=('Arial', 9, 'bold'), bg='#e0e0e0', 
                width=8, relief=tk.FLAT, bd=0, padx=2, pady=3).grid(row=0, column=0, sticky='ew')
        tk.Label(header_frame, text="Ele", font=('Arial', 9, 'bold'), bg='#e0e0e0', 
                width=10, relief=tk.FLAT, bd=0, padx=2, pady=3).grid(row=0, column=1, sticky='ew')
        tk.Label(header_frame, text="ATT", font=('Arial', 9, 'bold'), bg='#e0e0e0', 
                width=8, relief=tk.FLAT, bd=0, padx=2, pady=3).grid(row=0, column=2, sticky='ew')
        
        # Create data rows with cleaner borders
        for idx, (ele_name, ele_value, att_value) in enumerate(data):
            row = idx + 1
            
            # Alternate row colors for better readability
            row_bg = '#ffffff' if idx % 2 == 0 else '#f5f5f5'
            
            # Element name (read-only but user can type in empty ones)
            if ele_name:  # Pre-filled elements are read-only
                ele_name_widget = tk.Label(
                    table_container, 
                    text=ele_name, 
                    font=('Arial', 9), 
                    bg=row_bg,
                    relief=tk.FLAT,
                    bd=0,
                    anchor='center',
                    padx=2,
                    pady=2
                )
            else:  # Empty cells are editable
                ele_name_widget = tk.Entry(
                    table_container,
                    font=('Arial', 9),
                    justify='center',
                    relief=tk.FLAT,
                    bd=1,
                    bg='white'
                )
            ele_name_widget.grid(row=row, column=0, sticky='ew', padx=1, pady=1)
            
            # Element value (read-only but user can type in empty ones)
            if ele_value:  # Pre-filled values are read-only
                ele_value_widget = tk.Label(
                    table_container, 
                    text=ele_value, 
                    font=('Arial', 9), 
                    bg=row_bg,
                    relief=tk.FLAT,
                    bd=0,
                    anchor='center',
                    padx=2,
                    pady=2
                )
            else:  # Empty cells are editable
                ele_value_widget = tk.Entry(
                    table_container,
                    font=('Arial', 9),
                    justify='center',
                    relief=tk.FLAT,
                    bd=1,
                    bg='white'
                )
            ele_value_widget.grid(row=row, column=1, sticky='ew', padx=1, pady=1)
            
            # ATT value (always editable)
            att_entry = tk.Entry(
                table_container,
                font=('Arial', 9),
                justify='center',
                relief=tk.FLAT,
                bd=1,
                bg='white'
            )
            att_entry.insert(0, att_value)
            att_entry.grid(row=row, column=2, sticky='ew', padx=1, pady=1)
            
            # Store entry widget with element info
            att_entries_list.append({
                'element': ele_name,
                'ele_value': ele_value,
                'att_entry': att_entry,
                'ele_name_widget': ele_name_widget if isinstance(ele_name_widget, tk.Entry) else None,
                'ele_value_widget': ele_value_widget if isinstance(ele_value_widget, tk.Entry) else None
            })
        
        # Configure column weights for better distribution
        table_container.columnconfigure(0, weight=1, minsize=80)
        table_container.columnconfigure(1, weight=1, minsize=100)
        table_container.columnconfigure(2, weight=1, minsize=80)
    
    def collect_form_data(self):
        """Collect all form data into a unified JSON format"""
        
        left_table_data = []
        for entry_info in self.left_att_entries:
            # Get element name (from label or entry widget)
            element = entry_info['element']
            if entry_info.get('ele_name_widget'):
                element = entry_info['ele_name_widget'].get()
            
            # Get element value (from label or entry widget)
            ele_value = entry_info['ele_value']
            if entry_info.get('ele_value_widget'):
                ele_value = entry_info['ele_value_widget'].get()
            
            left_table_data.append({
                "element": element,
                "ele_value": ele_value,
                "att_value": entry_info['att_entry'].get()
            })
        
        right_table_data = []
        for entry_info in self.right_att_entries:
            # Get element name (from label or entry widget)
            element = entry_info['element']
            if entry_info.get('ele_name_widget'):
                element = entry_info['ele_name_widget'].get()
            
            # Get element value (from label or entry widget)
            ele_value = entry_info['ele_value']
            if entry_info.get('ele_value_widget'):
                ele_value = entry_info['ele_value_widget'].get()
            
            right_table_data.append({
                "element": element,
                "ele_value": ele_value,
                "att_value": entry_info['att_entry'].get()
            })
        
        form_data = {
            "analytical_group": self.selected_group,
            "page": "attenuator_information",
            "left_table": left_table_data,
            "right_table": right_table_data
        }
        
        return form_data
    
    def load_saved_data(self):
        """Load previously saved data if exists"""
        saved_data = self.data_manager.get_attenuator_information()
        if not saved_data:
            return
        
        # Load left table data
        if 'left_table' in saved_data:
            for idx, entry_info in enumerate(self.left_att_entries):
                if idx < len(saved_data['left_table']):
                    saved_row = saved_data['left_table'][idx]
                    
                    # Load element name if editable
                    if entry_info.get('ele_name_widget'):
                        entry_info['ele_name_widget'].delete(0, tk.END)
                        entry_info['ele_name_widget'].insert(0, saved_row.get('element', ''))
                    
                    # Load element value if editable
                    if entry_info.get('ele_value_widget'):
                        entry_info['ele_value_widget'].delete(0, tk.END)
                        entry_info['ele_value_widget'].insert(0, saved_row.get('ele_value', ''))
                    
                    # Load ATT value
                    att_value = saved_row.get('att_value', '')
                    entry_info['att_entry'].delete(0, tk.END)
                    entry_info['att_entry'].insert(0, att_value)
        
        # Load right table data
        if 'right_table' in saved_data:
            for idx, entry_info in enumerate(self.right_att_entries):
                if idx < len(saved_data['right_table']):
                    saved_row = saved_data['right_table'][idx]
                    
                    # Load element name if editable
                    if entry_info.get('ele_name_widget'):
                        entry_info['ele_name_widget'].delete(0, tk.END)
                        entry_info['ele_name_widget'].insert(0, saved_row.get('element', ''))
                    
                    # Load element value if editable
                    if entry_info.get('ele_value_widget'):
                        entry_info['ele_value_widget'].delete(0, tk.END)
                        entry_info['ele_value_widget'].insert(0, saved_row.get('ele_value', ''))
                    
                    # Load ATT value
                    att_value = saved_row.get('att_value', '')
                    entry_info['att_entry'].delete(0, tk.END)
                    entry_info['att_entry'].insert(0, att_value)
    
    def save_current_data(self):
        """Save current form data before leaving page"""
        form_data = self.collect_form_data()
        self.data_manager.save_attenuator_information(form_data)
    
    def on_upload_clicked(self):
        """Handler for Upload button - Collects and prepares data for POST request"""
        try:
            # Collect all form data
            form_data = self.collect_form_data()
            
            # Convert to JSON
            json_data = json.dumps(form_data, indent=2)
            
            # For now, just display the JSON (backend not ready)
            print("\n" + "="*50)
            print("ATTENUATOR INFORMATION - JSON DATA TO BE SENT:")
            print("="*50)
            print(json_data)
            print("="*50 + "\n")
            
            # Show success message with preview
            messagebox.showinfo(
                "Upload Ready", 
                f"Attenuator data collected successfully!\n\nJSON Preview:\n{json_data[:150]}...\n\n(Full JSON printed to console)\n\nReady for POST request to backend."
            )
            
            # TODO: When backend is ready, uncomment this:
            # import requests
            # response = requests.post('http://your-backend-url/api/attenuator-information', json=form_data)
            # if response.status_code == 200:
            #     messagebox.showinfo("Success", "Data uploaded successfully!")
            # else:
            #     messagebox.showerror("Error", f"Upload failed: {response.status_code}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to collect data: {str(e)}")
    
    def on_ok_clicked(self):
        """Handler for OK button"""
        self.save_current_data()
        messagebox.showinfo("OK", "Attenuator information saved successfully!")
    
    def on_next_clicked(self):
        """Handler for Next button - Navigate to next page"""
        self.save_current_data()
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        # Open Element Information page
        ElementInformationPage(self.parent_frame, self.selected_group, self)
    
    def on_pre_clicked(self):
        """Handler for Pre. button - Go back to previous page"""
        self.save_current_data()
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Reopen previous page (Analytical Condition)
        from pages.analytical_condition import AnalyticalConditionPage
        AnalyticalConditionPage(self.parent_frame, self.selected_group, self.parent_app)
    
    def on_print_clicked(self):
        """Handler for Print button"""
        messagebox.showinfo("Print", "Printing attenuator information...")
    
    def on_cancel_clicked(self):
        """Handler for Cancel button"""
        confirm = messagebox.askyesno("Cancel", "Are you sure you want to cancel? Changes will not be saved.")
        if confirm:
            for widget in self.parent_frame.winfo_children():
                widget.destroy()
