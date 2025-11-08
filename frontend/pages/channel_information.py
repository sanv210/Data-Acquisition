import tkinter as tk
from tkinter import ttk, messagebox
import json
from utils.data_manager import DataManager


class ChannelInformationPage:
    def __init__(self, parent_frame, selected_group, parent_app=None):
        self.parent_frame = parent_frame
        self.selected_group = selected_group
        self.parent_app = parent_app
        self.data_manager = DataManager()
        
        # Store entry widgets for data collection
        self.channel_entries = []
        
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
            text=f"Channel Information - {self.selected_group}",
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
        
        # Split into left and right panels
        left_right_frame = tk.Frame(content_frame, bg='#d4d0c8')
        left_right_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Analytical Group list
        left_panel = tk.Frame(left_right_frame, bg='#d4d0c8', relief=tk.RAISED, bd=2, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.create_left_panel(left_panel)
        
        # Right panel - Channel table
        right_panel = tk.Frame(left_right_frame, bg='#d4d0c8')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_right_panel(right_panel)
        
        # Bottom buttons
        button_frame = tk.Frame(main_frame, bg='#d4d0c8')
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
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
        
        ele_btn = tk.Button(left_buttons, text="6.Ele.", command=self.on_ele_clicked, **button_config)
        ele_btn.pack(side=tk.LEFT, padx=3)
        
        # Upload button
        upload_btn = tk.Button(left_buttons, text="Upload", command=self.on_upload_clicked, **button_config)
        upload_btn.pack(side=tk.LEFT, padx=3)
        
        # Right side button
        right_buttons = tk.Frame(button_frame, bg='#d4d0c8')
        right_buttons.pack(side=tk.RIGHT)
        
        cancel_btn = tk.Button(right_buttons, text="9.Cancel", command=self.on_cancel_clicked, **button_config)
        cancel_btn.pack(side=tk.RIGHT, padx=3)
    
    def create_left_panel(self, parent):
        """Create the left panel with Analytical Group list"""
        list_label = tk.Label(
            parent,
            text="Analytical Group",
            font=('Arial', 9),
            bg='#d4d0c8'
        )
        list_label.pack(pady=(5, 2))
        
        # Listbox with scrollbar
        list_frame = tk.Frame(parent)
        list_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.analytical_listbox = tk.Listbox(
            list_frame,
            font=('Arial', 9),
            bg='white',
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            width=20
        )
        self.analytical_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.analytical_listbox.yview)
        
        # Populate the listbox
        analytical_groups = [
            "LAS 2023", "SS 2023", "LA 2021", "SS - 2022", "FERR 2022",
            "TOLL STEEL2021", "FERR 2020", "SS 2021", "LA 2021 S",
            "GLOBAL CAL", "LA 2020", "LA-WITH HI MN", "SS WITH HI MN",
            "Cast", "LOW-ALLOY-HS", "NI 2017", "INCONEL 17", "MONEL 17",
            "TEST GROUP", "LA 2021 WITH CA", "TEST LAS", "26-11-22",
            "FERR 2023", "GHHaj"
        ]
        
        for group in analytical_groups:
            self.analytical_listbox.insert(tk.END, group)
        
        # Select the current group
        try:
            idx = analytical_groups.index(self.selected_group)
            self.analytical_listbox.selection_set(idx)
            self.analytical_listbox.see(idx)
        except ValueError:
            self.analytical_listbox.selection_set(0)
        
        # Buttons
        button_panel = tk.Frame(parent, bg='#d4d0c8')
        button_panel.pack(pady=10, padx=10, fill=tk.X)
        
        button_config = {
            'width': 12,
            'font': ('Arial', 9),
            'bg': '#d4d0c8',
            'relief': tk.RAISED,
            'bd': 2
        }
        
        select_btn = tk.Button(button_panel, text="1.Select", command=self.on_select_group, **button_config)
        select_btn.pack(pady=2, fill=tk.X)
        
        detail_btn = tk.Button(button_panel, text="2.Detail", command=self.on_detail_group, **button_config)
        detail_btn.pack(pady=2, fill=tk.X)
        
        arrange_btn = tk.Button(button_panel, text="9.Arrange", command=self.on_arrange_group, **button_config)
        arrange_btn.pack(pady=2, fill=tk.X)
        
        new_btn = tk.Button(button_panel, text="6.New", command=self.on_new_group, **button_config)
        new_btn.pack(pady=2, fill=tk.X)
        
        delete_btn = tk.Button(button_panel, text="8.Delete", command=self.on_delete_group, **button_config)
        delete_btn.pack(pady=2, fill=tk.X)
        
        wc_cost_btn = tk.Button(button_panel, text="9.WC Cost Copy", command=self.on_wc_cost_copy, **button_config)
        wc_cost_btn.pack(pady=2, fill=tk.X)
    
    def create_right_panel(self, parent):
        """Create the right panel with channel table"""
        # Table frame with scrollbar
        table_container = tk.Frame(parent, bg='white', relief=tk.SOLID, bd=1)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for scrolling
        canvas = tk.Canvas(table_container, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(table_container, orient="vertical", command=canvas.yview)
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
        
        # Create table
        self.create_channel_table(scrollable_frame)
        
        # Bottom buttons for table
        table_buttons = tk.Frame(parent, bg='#d4d0c8')
        table_buttons.pack(fill=tk.X, pady=(5, 0))
        
        button_config = {
            'width': 12,
            'font': ('Arial', 9),
            'bg': '#d4d0c8',
            'relief': tk.RAISED,
            'bd': 2
        }
        
        add_btn = tk.Button(table_buttons, text="S2.Add", command=self.on_add_row, **button_config)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        new_btn = tk.Button(table_buttons, text="S3.New", command=self.on_new_row, **button_config)
        new_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(table_buttons, text="S4.Delete", command=self.on_delete_row, **button_config)
        delete_btn.pack(side=tk.LEFT, padx=5)
    
    def create_channel_table(self, parent):
        """Create the channel information table"""
        # Channel data from images
        channels_data = [
            ("Fe", "396.8", "1", "", "FE", "273.0"),
            ("C", "193.0", "2", "", "FE", "273.0"),
            ("Si", "212.4", "2", "", "FE", "273.0"),
            ("Mn", "293.3", "2", "", "FE", "273.0"),
            ("P", "178.3", "1", "", "FE", "273.0"),
            ("S", "180.7", "1", "", "FE", "273.0"),
            ("Cr", "267.7", "2", "", "FE", "273.0"),
            ("Ni", "231.6", "2", "", "FE", "273.0"),
            ("Mo", "202.0", "2", "", "FE", "273.0"),
            ("Cu", "224.2", "2", "", "FE", "273.0"),
            ("V", "311.0", "2", "", "FE", "273.0"),
            ("Ti", "337.2", "1", "", "FE", "273.0"),
            ("W", "220.4", "2", "", "FE", "273.0"),
            ("B", "182.6", "1", "", "FE", "273.0"),
            ("Nb", "319.5", "2", "", "FE", "273.0"),
            ("Ca", "396.8", "1", "", "FE", "273.0"),
            ("Co", "258.0", "2", "", "FE", "273.0"),
            ("Sn", "189.9", "2", "", "FE", "273.0"),
            ("N", "174.5+2", "2", "", "FE", "273.0"),
            ("Pb", "405.7", "1", "", "FE", "273.0"),
            ("Al", "394.4", "1", "", "FE", "273.0"),
            ("CE", "", "1", "", "FE", "273.0"),
        ]
        
        # Header
        header_frame = tk.Frame(parent, bg='#e8e8e8', relief=tk.RIDGE, bd=1)
        header_frame.grid(row=0, column=0, columnspan=6, sticky='ew')
        
        # Configure grid for header
        for i in range(6):
            header_frame.columnconfigure(i, weight=1)
        
        headers = [
            ("Ele Name", 0, 1),
            ("W.Lengh", 1, 1),
            ("SEQ", 2, 1),
            ("W.No", 3, 1),
            ("Interval Element", 4, 2)  # Spans 2 columns
        ]
        
        for header_text, col, colspan in headers:
            tk.Label(
                header_frame,
                text=header_text,
                font=('Arial', 9, 'bold'),
                bg='#e8e8e8',
                relief=tk.FLAT,
                bd=0,
                padx=5,
                pady=3
            ).grid(row=0, column=col, columnspan=colspan, sticky='ew')
        
        # Data rows
        for idx, (ele_name, w_lengh, seq, w_no, interval_ele, interval_val) in enumerate(channels_data):
            row = idx + 1
            
            # Ele Name (editable)
            ele_name_entry = tk.Entry(
                parent,
                font=('Arial', 9),
                justify='center',
                relief=tk.SOLID,
                bd=1,
                bg='white'
            )
            ele_name_entry.insert(0, ele_name)
            ele_name_entry.grid(row=row, column=0, sticky='ew', padx=0, pady=0)
            
            # W.Lengh (editable)
            w_lengh_entry = tk.Entry(
                parent,
                font=('Arial', 9),
                justify='right',
                relief=tk.SOLID,
                bd=1,
                bg='white'
            )
            w_lengh_entry.insert(0, w_lengh)
            w_lengh_entry.grid(row=row, column=1, sticky='ew', padx=0, pady=0)
            
            # SEQ (editable)
            seq_entry = tk.Entry(
                parent,
                font=('Arial', 9),
                justify='center',
                relief=tk.SOLID,
                bd=1,
                bg='white'
            )
            seq_entry.insert(0, seq)
            seq_entry.grid(row=row, column=2, sticky='ew', padx=0, pady=0)
            
            # W.No (editable)
            w_no_entry = tk.Entry(
                parent,
                font=('Arial', 9),
                justify='center',
                relief=tk.SOLID,
                bd=1,
                bg='white'
            )
            w_no_entry.insert(0, w_no)
            w_no_entry.grid(row=row, column=3, sticky='ew', padx=0, pady=0)
            
            # Interval Element (editable)
            interval_ele_entry = tk.Entry(
                parent,
                font=('Arial', 9),
                justify='center',
                relief=tk.SOLID,
                bd=1,
                bg='white'
            )
            interval_ele_entry.insert(0, interval_ele)
            interval_ele_entry.grid(row=row, column=4, sticky='ew', padx=0, pady=0)
            
            # Interval Value (editable)
            interval_val_entry = tk.Entry(
                parent,
                font=('Arial', 9),
                justify='right',
                relief=tk.SOLID,
                bd=1,
                bg='white'
            )
            interval_val_entry.insert(0, interval_val)
            interval_val_entry.grid(row=row, column=5, sticky='ew', padx=0, pady=0)
            
            # Store all entries
            self.channel_entries.append({
                'ele_name': ele_name_entry,
                'w_lengh': w_lengh_entry,
                'seq': seq_entry,
                'w_no': w_no_entry,
                'interval_ele': interval_ele_entry,
                'interval_val': interval_val_entry
            })
        
        # Configure column weights
        parent.columnconfigure(0, weight=1, minsize=80)   # Ele Name
        parent.columnconfigure(1, weight=1, minsize=100)  # W.Lengh
        parent.columnconfigure(2, weight=0, minsize=50)   # SEQ
        parent.columnconfigure(3, weight=1, minsize=80)   # W.No
        parent.columnconfigure(4, weight=1, minsize=80)   # Interval Ele
        parent.columnconfigure(5, weight=1, minsize=80)   # Interval Val
    
    def collect_form_data(self):
        """Collect all form data into a unified JSON format"""
        channels_data = []
        
        for entry_info in self.channel_entries:
            channels_data.append({
                "ele_name": entry_info['ele_name'].get(),
                "w_lengh": entry_info['w_lengh'].get(),
                "seq": entry_info['seq'].get(),
                "w_no": entry_info['w_no'].get(),
                "interval_element": entry_info['interval_ele'].get(),
                "interval_value": entry_info['interval_val'].get()
            })
        
        form_data = {
            "analytical_group": self.selected_group,
            "page": "channel_information",
            "channels": channels_data
        }
        
        return form_data
    
    def load_saved_data(self):
        """Load previously saved data if exists"""
        # TODO: Implement when data manager is extended
        pass
    
    def save_current_data(self):
        """Save current form data before leaving page"""
        form_data = self.collect_form_data()
        # TODO: Add to data manager when extended
    
    def on_upload_clicked(self):
        """Handler for Upload button - Uploads data to backend API"""
        try:
            form_data = self.collect_form_data()
            json_data = json.dumps(form_data, indent=2)
            
            print("\n" + "="*50)
            print("CHANNEL INFORMATION - UPLOADING TO BACKEND:")
            print("="*50)
            print(json_data)
            print("="*50 + "\n")
            
            # Upload to backend API
            response = self.data_manager.upload_channel_information(form_data)
            
            # Show success message with API response
            if response and 'records' in response:
                created_record = response['records'][0]
                record_id = created_record.get('id', 'N/A')
                channel_count = len(form_data.get('channels', []))
                messagebox.showinfo(
                    "Upload Successful",
                    f"Channel Information uploaded successfully!\n\n"
                    f"Record ID: {record_id}\n"
                    f"Analytical Group: {self.selected_group}\n"
                    f"Channels: {channel_count}\n\n"
                    f"Data saved to database."
                )
            else:
                messagebox.showinfo(
                    "Upload Complete",
                    f"{len(self.channel_entries)} channels uploaded successfully!"
                )
            
        except Exception as e:
            messagebox.showerror(
                "Upload Failed",
                f"Failed to upload data to backend:\n\n{str(e)}\n\n"
                f"Please ensure the backend server is running on http://localhost:8000"
            )
    
    def on_ok_clicked(self):
        """Handler for OK button"""
        self.save_current_data()
        messagebox.showinfo("OK", "Channel information saved successfully!")
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
    
    def on_next_clicked(self):
        """Handler for Next button"""
        self.save_current_data()
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        messagebox.showinfo("Next", "End of form sequence!")
        # This is the last page in the sequence
    
    def on_pre_clicked(self):
        """Handler for Pre. button"""
        self.save_current_data()
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        # Go back to Element Information
        from pages.element_information import ElementInformationPage
        ElementInformationPage(self.root, self.selected_group, self.parent_app)
    
    def on_print_clicked(self):
        """Handler for Print button"""
        messagebox.showinfo("Print", "Printing channel information...")
    
    def on_ele_clicked(self):
        """Handler for Ele. button"""
        messagebox.showinfo("Ele.", "Element functionality...")
    
    def on_cancel_clicked(self):
        """Handler for Cancel button"""
        confirm = messagebox.askyesno("Cancel", "Are you sure you want to cancel?")
        if confirm:
            for widget in self.parent_frame.winfo_children():
                widget.destroy()
    
    def on_select_group(self):
        """Handler for selecting a group from the list"""
        selection = self.analytical_listbox.curselection()
        if selection:
            selected = self.analytical_listbox.get(selection[0])
            messagebox.showinfo("Select", f"Selected: {selected}")
    
    def on_detail_group(self):
        """Handler for Detail button"""
        messagebox.showinfo("Detail", "Group detail...")
    
    def on_arrange_group(self):
        """Handler for Arrange button"""
        messagebox.showinfo("Arrange", "Arrange groups...")
    
    def on_new_group(self):
        """Handler for New button"""
        messagebox.showinfo("New", "Create new group...")
    
    def on_delete_group(self):
        """Handler for Delete button"""
        messagebox.showinfo("Delete", "Delete group...")
    
    def on_wc_cost_copy(self):
        """Handler for WC Cost Copy button"""
        messagebox.showinfo("WC Cost Copy", "Copy WC cost...")
    
    def on_add_row(self):
        """Handler for S2.Add button"""
        messagebox.showinfo("Add", "Add new channel...")
    
    def on_new_row(self):
        """Handler for S3.New button"""
        messagebox.showinfo("New", "Create new channel...")
    
    def on_delete_row(self):
        """Handler for S4.Delete button"""
        messagebox.showinfo("Delete", "Delete selected channel...")
