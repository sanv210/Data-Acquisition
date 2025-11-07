import tkinter as tk
from tkinter import ttk, messagebox
import json
from utils.data_manager import DataManager
from pages.channel_information import ChannelInformationPage


class ElementInformationPage:
    def __init__(self, parent_frame, selected_group, parent_app=None):
        self.parent_frame = parent_frame
        self.selected_group = selected_group
        self.parent_app = parent_app
        self.data_manager = DataManager()
        
        # Store entry widgets for data collection
        self.element_entries = []
        
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
            text=f"Element Information - {self.selected_group}",
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
        
        # Right panel - Element table
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
        """Create the right panel with element table"""
        # Top section with CH 22
        top_section = tk.Frame(parent, bg='#d4d0c8')
        top_section.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(top_section, text="CH", font=('Arial', 9), bg='#d4d0c8').pack(side=tk.LEFT, padx=(0, 5))
        
        # CH value as read-only label styled like entry
        ch_label = tk.Label(
            top_section, 
            text="22", 
            font=('Arial', 9), 
            bg='white',
            relief=tk.SUNKEN,
            bd=1,
            width=5,
            anchor='center'
        )
        ch_label.pack(side=tk.LEFT)
        
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
        self.create_element_table(scrollable_frame)
        
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
        
        insert_btn = tk.Button(table_buttons, text="S3.Insert", command=self.on_insert_row, **button_config)
        insert_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(table_buttons, text="S4.Delete", command=self.on_delete_row, **button_config)
        delete_btn.pack(side=tk.LEFT, padx=5)
    
    def create_element_table(self, parent):
        """Create the element information table"""
        # Element data
        elements_data = [
            ("Fe", ".00000", "100.00", "*", "Fe", "Fe"),
            ("C", ".00000", "100.00", "*", "C", "C"),
            ("Si", ".00000", "100.00", "*", "Si", "Si"),
            ("Mn", ".00000", "100.00", "*", "Mn", "Mn"),
            ("P", ".00000", "100.00", "*", "P", "P"),
            ("S", ".00000", "100.00", "*", "S", "S"),
            ("Cr", ".00000", "100.00", "*", "Cr", "Cr"),
            ("Ni", ".00000", "100.00", "*", "Ni", "Ni"),
            ("Mo", ".00000", "100.00", "*", "Mo", "Mo"),
            ("Cu", ".00000", "100.00", "*", "Cu", "Cu"),
            ("V", ".00000", "100.00", "*", "V", "V"),
            ("Ti", ".00000", "100.00", "*", "Ti", "Ti"),
            ("W", ".00000", "100.00", "*", "W", "W"),
            ("B", ".00000", "100.00", "*", "B", "B"),
            ("Nb", ".00000", "100.00", "*", "Nb", "Nb"),
            ("Ca", ".00000", "100.00", "*", "Ca", "Ca"),
            ("Co", ".00000", "100.00", "*", "Co", "Co"),
            ("Sn", ".00000", "100.00", "*", "Sn", "Sn"),
            ("N", ".00000", "100.00", "*", "N", "N"),
            ("Pb", ".00000", "100.00", "*", "Pb", "Pb"),
            ("Al", ".00000", "100.00", "*", "Al", "AL"),
            ("CE", ".00000", ".00000", "*", "", ""),
            ("", ".00000", ".00000", "", "", ""),
        ]
        
        # Header frame with proper spanning
        header_frame = tk.Frame(parent, bg='#e8e8e8', relief=tk.RIDGE, bd=1)
        header_frame.grid(row=0, column=0, columnspan=6, sticky='ew')
        
        # Configure grid for header
        for i in range(6):
            header_frame.columnconfigure(i, weight=1)
        
        # Ele Name header
        tk.Label(
            header_frame, 
            text="Ele Name", 
            font=('Arial', 9, 'bold'), 
            bg='#e8e8e8',
            relief=tk.FLAT,
            bd=0,
            padx=5,
            pady=3
        ).grid(row=0, column=0, sticky='ew')
        
        # Analytical Rang header (spans 2 columns)
        tk.Label(
            header_frame, 
            text="analytical Rang", 
            font=('Arial', 9, 'bold'), 
            bg='#e8e8e8',
            relief=tk.FLAT,
            bd=0,
            padx=5,
            pady=3
        ).grid(row=0, column=1, columnspan=2, sticky='ew')
        
        # * header
        tk.Label(
            header_frame, 
            text="*", 
            font=('Arial', 9, 'bold'), 
            bg='#e8e8e8',
            relief=tk.FLAT,
            bd=0,
            padx=5,
            pady=3
        ).grid(row=0, column=3, sticky='ew')
        
        # Chemic Ele header
        tk.Label(
            header_frame, 
            text="Chemic Ele", 
            font=('Arial', 9, 'bold'), 
            bg='#e8e8e8',
            relief=tk.FLAT,
            bd=0,
            padx=5,
            pady=3
        ).grid(row=0, column=4, sticky='ew')
        
        # Element header
        tk.Label(
            header_frame, 
            text="Element", 
            font=('Arial', 9, 'bold'), 
            bg='#e8e8e8',
            relief=tk.FLAT,
            bd=0,
            padx=5,
            pady=3
        ).grid(row=0, column=5, sticky='ew')
        
        # Data rows - all with white background
        for idx, (ele_name, range1, range2, asterisk, chem_ele, element) in enumerate(elements_data):
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
            
            # Analytical Range 1 (editable)
            range1_entry = tk.Entry(
                parent, 
                font=('Arial', 9), 
                justify='right', 
                relief=tk.SOLID, 
                bd=1, 
                bg='white'
            )
            range1_entry.insert(0, range1)
            range1_entry.grid(row=row, column=1, sticky='ew', padx=0, pady=0)
            
            # Analytical Range 2 (editable)
            range2_entry = tk.Entry(
                parent, 
                font=('Arial', 9), 
                justify='right', 
                relief=tk.SOLID, 
                bd=1, 
                bg='white'
            )
            range2_entry.insert(0, range2)
            range2_entry.grid(row=row, column=2, sticky='ew', padx=0, pady=0)
            
            # Asterisk (editable)
            asterisk_entry = tk.Entry(
                parent, 
                font=('Arial', 9), 
                justify='center', 
                relief=tk.SOLID, 
                bd=1, 
                bg='white'
            )
            asterisk_entry.insert(0, asterisk)
            asterisk_entry.grid(row=row, column=3, sticky='ew', padx=0, pady=0)
            
            # Chemic Ele (editable)
            chem_ele_entry = tk.Entry(
                parent, 
                font=('Arial', 9), 
                justify='center', 
                relief=tk.SOLID, 
                bd=1, 
                bg='white'
            )
            chem_ele_entry.insert(0, chem_ele)
            chem_ele_entry.grid(row=row, column=4, sticky='ew', padx=0, pady=0)
            
            # Element (editable)
            element_entry = tk.Entry(
                parent, 
                font=('Arial', 9), 
                justify='center', 
                relief=tk.SOLID, 
                bd=1, 
                bg='white'
            )
            element_entry.insert(0, element)
            element_entry.grid(row=row, column=5, sticky='ew', padx=0, pady=0)
            
            # Store all entries
            self.element_entries.append({
                'ele_name': ele_name_entry,
                'range1': range1_entry,
                'range2': range2_entry,
                'asterisk': asterisk_entry,
                'chem_ele': chem_ele_entry,
                'element': element_entry
            })
        
        # Configure column weights for proper sizing
        parent.columnconfigure(0, weight=1, minsize=80)   # Ele Name
        parent.columnconfigure(1, weight=1, minsize=100)  # Range 1
        parent.columnconfigure(2, weight=1, minsize=100)  # Range 2
        parent.columnconfigure(3, weight=0, minsize=40)   # *
        parent.columnconfigure(4, weight=1, minsize=100)  # Chemic Ele
        parent.columnconfigure(5, weight=1, minsize=80)   # Element
    
    def collect_form_data(self):
        """Collect all form data into a unified JSON format"""
        elements_data = []
        
        for entry_info in self.element_entries:
            elements_data.append({
                "ele_name": entry_info['ele_name'].get(),
                "analytical_range_min": entry_info['range1'].get(),
                "analytical_range_max": entry_info['range2'].get(),
                "asterisk": entry_info['asterisk'].get(),
                "chemic_ele": entry_info['chem_ele'].get(),
                "element": entry_info['element'].get()
            })
        
        form_data = {
            "analytical_group": self.selected_group,
            "page": "element_information",
            "ch_value": "22",
            "elements": elements_data
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
        """Handler for Upload button"""
        try:
            form_data = self.collect_form_data()
            json_data = json.dumps(form_data, indent=2)
            
            print("\n" + "="*50)
            print("ELEMENT INFORMATION - JSON DATA:")
            print("="*50)
            print(json_data)
            print("="*50 + "\n")
            
            messagebox.showinfo(
                "Upload Ready",
                f"Element data collected successfully!\n\n{len(self.element_entries)} elements ready for upload.\n\n(Full JSON printed to console)"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to collect data: {str(e)}")
    
    def on_ok_clicked(self):
        """Handler for OK button"""
        self.save_current_data()
        messagebox.showinfo("OK", "Element information saved successfully!")
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
    
    def on_next_clicked(self):
        """Handler for Next button"""
        self.save_current_data()
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        # Open Channel Information page
        ChannelInformationPage(self.parent_frame, self.selected_group, self)
    
    def on_pre_clicked(self):
        """Handler for Pre. button"""
        self.save_current_data()
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        # Go back to Attenuator Information
        from pages.attenuator_information import AttenuatorInformationPage
        AttenuatorInformationPage(self.parent_frame, self.selected_group, self.parent_app)
    
    def on_print_clicked(self):
        """Handler for Print button"""
        messagebox.showinfo("Print", "Printing element information...")
    
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
    
    def on_insert_row(self):
        """Handler for S3.Insert button"""
        messagebox.showinfo("Insert", "Insert new row...")
    
    def on_delete_row(self):
        """Handler for S4.Delete button"""
        messagebox.showinfo("Delete", "Delete selected row...")
