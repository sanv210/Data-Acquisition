import tkinter as tk
from tkinter import ttk, messagebox
import json
from pages.attenuator_information import AttenuatorInformationPage
from utils.data_manager import DataManager


class AnalyticalConditionPage:
    def __init__(self, parent_frame, selected_group, parent_app=None):
        self.parent_frame = parent_frame
        self.selected_group = selected_group
        self.parent_app = parent_app
        self.data_manager = DataManager()

        self.frame = tk.Frame(self.parent_frame, bg='#d4d0c8')
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        self.load_saved_data()
        
    def create_widgets(self):
        # Main container frame
        main_frame = tk.Frame(self.frame, bg='#d4d0c8')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title Frame
        title_frame = tk.Frame(main_frame, bg='#5c9bd5', relief=tk.RAISED, bd=2)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text=f"Analytical Condition - {self.selected_group}",
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
        
        # Analytical Method Section
        method_frame = tk.LabelFrame(inner_frame, text="Analytical Method", font=('Arial', 9), bg='#d4d0c8')
        method_frame.pack(fill=tk.X, pady=(0, 10))
        
        method_inner = tk.Frame(method_frame, bg='#d4d0c8')
        method_inner.pack(fill=tk.X, padx=10, pady=5)
        
        self.analytical_method = ttk.Combobox(
            method_inner,
            values=["integration Mode", "PDA + Integration"],
            state='readonly',
            width=35,
            font=('Arial', 9)
        )
        self.analytical_method.set("integration Mode")
        self.analytical_method.pack()
        
        # SEQ Section
        seq_frame = tk.LabelFrame(inner_frame, text="SEQ", font=('Arial', 9), bg='#d4d0c8')
        seq_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        seq_inner = tk.Frame(seq_frame, bg='#d4d0c8')
        seq_inner.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Header row
        headers = ["", "SEQ1", "SEQ2", "SEQ3", "Clean"]
        for col, header in enumerate(headers):
            if col == 0:
                continue
            label = tk.Label(seq_inner, text=header, font=('Arial', 9), bg='#d4d0c8', width=12)
            label.grid(row=0, column=col, padx=2, pady=2)
        
        # Sec. label
        sec_label = tk.Label(seq_inner, text="Sec.", font=('Arial', 9), bg='#d4d0c8', anchor='e')
        sec_label.grid(row=0, column=5, padx=2, pady=2, sticky='e')
        
        # Purge row
        tk.Label(seq_inner, text="Purge", font=('Arial', 9), bg='#d4d0c8', anchor='w').grid(row=1, column=0, sticky='w', padx=2)
        self.purge_seq1 = tk.Entry(seq_inner, width=12, font=('Arial', 9))
        self.purge_seq1.insert(0, "3")
        self.purge_seq1.grid(row=1, column=1, padx=2, pady=2)
        
        # Source row
        tk.Label(seq_inner, text="Source", font=('Arial', 9), bg='#d4d0c8', anchor='w').grid(row=2, column=0, sticky='w', padx=2)
        
        self.source_seq1 = ttk.Combobox(seq_inner, values=[
            "3 Peak Spark", "Normal Spark", "Combined Spark", "Arclike Spark", "Cleaning", "High Voltage Spark"
        ], state='readonly', width=18, font=('Arial', 8))
        self.source_seq1.set("3 Peak Spark")
        self.source_seq1.grid(row=2, column=1, padx=2, pady=2)
        
        self.source_seq2 = ttk.Combobox(seq_inner, values=[
            "Normal Spark", "Combined Spark", "Arclike Spark", "Cleaning", "High Voltage Spark", "AD OFFSET"
        ], state='readonly', width=18, font=('Arial', 8))
        self.source_seq2.set("Normal Spark")
        self.source_seq2.grid(row=2, column=2, padx=2, pady=2)
        
        self.source_seq3 = ttk.Combobox(seq_inner, values=[
            "Lamp", "3 Peak Spark", "Normal Spark", "Combined Spark", "Arclike Spark", "Cleaning"
        ], state='readonly', width=18, font=('Arial', 8))
        self.source_seq3.set("Lamp")
        self.source_seq3.grid(row=2, column=3, padx=2, pady=2)
        
        self.source_clean = ttk.Combobox(seq_inner, values=[
            "Cleaning", "High Voltage Spark", "AD OFFSET", "ITG OFFSET", "MAIN OFFSET", "NOISE TEST"
        ], state='readonly', width=18, font=('Arial', 8))
        self.source_clean.set("Cleaning")
        self.source_clean.grid(row=2, column=4, padx=2, pady=2)
        
        # Preburn row
        tk.Label(seq_inner, text="Preburn", font=('Arial', 9), bg='#d4d0c8', anchor='w').grid(row=3, column=0, sticky='w', padx=2)
        self.preburn_seq1 = tk.Entry(seq_inner, width=12, font=('Arial', 9))
        self.preburn_seq1.insert(0, "100")
        self.preburn_seq1.grid(row=3, column=1, padx=2, pady=2)
        
        self.preburn_seq2 = tk.Entry(seq_inner, width=12, font=('Arial', 9))
        self.preburn_seq2.insert(0, "300")
        self.preburn_seq2.grid(row=3, column=2, padx=2, pady=2)
        
        self.preburn_seq3 = tk.Entry(seq_inner, width=12, font=('Arial', 9))
        self.preburn_seq3.insert(0, "0")
        self.preburn_seq3.grid(row=3, column=3, padx=2, pady=2)
        
        self.preburn_clean_label = tk.Label(seq_inner, text="Pulse", font=('Arial', 9), bg='#d4d0c8')
        self.preburn_clean_label.grid(row=3, column=4, padx=2, pady=2)
        
        # Integ row
        tk.Label(seq_inner, text="Integ", font=('Arial', 9), bg='#d4d0c8', anchor='w').grid(row=4, column=0, sticky='w', padx=2)
        self.integ_seq1 = tk.Entry(seq_inner, width=12, font=('Arial', 9))
        self.integ_seq1.insert(0, "300")
        self.integ_seq1.grid(row=4, column=1, padx=2, pady=2)
        
        self.integ_seq2 = tk.Entry(seq_inner, width=12, font=('Arial', 9))
        self.integ_seq2.insert(0, "23")
        self.integ_seq2.grid(row=4, column=2, padx=2, pady=2)
        
        self.integ_seq3 = tk.Entry(seq_inner, width=12, font=('Arial', 9))
        self.integ_seq3.insert(0, "0")
        self.integ_seq3.grid(row=4, column=3, padx=2, pady=2)
        
        self.integ_clean_label = tk.Label(seq_inner, text="Pulse", font=('Arial', 9), bg='#d4d0c8')
        self.integ_clean_label.grid(row=4, column=4, padx=2, pady=2)
        
        # Clean row
        tk.Label(seq_inner, text="Clean", font=('Arial', 9), bg='#d4d0c8', anchor='w').grid(row=5, column=0, sticky='w', padx=2)
        self.clean_entry = tk.Entry(seq_inner, width=12, font=('Arial', 9))
        self.clean_entry.insert(0, "0")
        self.clean_entry.grid(row=5, column=4, padx=2, pady=2)
        
        self.clean_pulse = tk.Label(seq_inner, text="Pulse", font=('Arial', 9), bg='#d4d0c8')
        self.clean_pulse.grid(row=5, column=5, padx=2, pady=2)
        
        # Level Out Information Section
        level_frame = tk.LabelFrame(inner_frame, text="Level Out Information", font=('Arial', 9), bg='#d4d0c8')
        level_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        level_inner = tk.Frame(level_frame, bg='#d4d0c8')
        level_inner.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Monitor Ele row
        monitor_row = tk.Frame(level_inner, bg='#d4d0c8')
        monitor_row.pack(fill=tk.X, pady=2)
        
        tk.Label(monitor_row, text="Monitor Ele.", font=('Arial', 9), bg='#d4d0c8', width=15, anchor='w').pack(side=tk.LEFT, padx=2)
        
        # Monitor element with default values mapping
        self.monitor_ele_values = {
            "None": "",
            "FE": "273.0",
            "C": "193.0",
            "Si": "212.4",
            "MN": "293.3",
            "P": "178.3",
            "S": "180.7",
            "V": "311.0",
            "CR": "267.7",
            "CR": "298.9"
        }
        
        self.monitor_ele = ttk.Combobox(monitor_row, values=list(self.monitor_ele_values.keys()), state='readonly', width=8, font=('Arial', 9))
        self.monitor_ele.set("FE")
        self.monitor_ele.bind("<<ComboboxSelected>>", self.on_monitor_ele_changed)
        self.monitor_ele.pack(side=tk.LEFT, padx=2)
        
        self.monitor_value = tk.Entry(monitor_row, width=10, font=('Arial', 9))
        self.monitor_value.insert(0, "273.0")
        self.monitor_value.pack(side=tk.LEFT, padx=2)
        
        self.monitor_none1 = ttk.Combobox(monitor_row, values=["None", "FE", "C", "Si", "MN", "P", "S", "V", "CR"], state='readonly', width=8, font=('Arial', 9))
        self.monitor_none1.set("None")
        self.monitor_none1.pack(side=tk.LEFT, padx=2)
        
        self.monitor_none2 = ttk.Combobox(monitor_row, values=["None", "FE", "C", "Si", "MN", "P", "S", "V", "CR"], state='readonly', width=8, font=('Arial', 9))
        self.monitor_none2.set("None")
        self.monitor_none2.pack(side=tk.LEFT, padx=2)
        
        # Table for SEQ levels
        table_frame = tk.Frame(level_inner, bg='#d4d0c8')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create table headers
        seq_headers = ["", "SEQ1", "SEQ2", "SEQ3", "SEQ1", "SEQ2", "SEQ3", "SEQ1", "SEQ2", "SEQ3"]
        for col, header in enumerate(seq_headers):
            label = tk.Label(table_frame, text=header, font=('Arial', 8), bg='#d4d0c8', relief=tk.RIDGE, width=8)
            label.grid(row=0, column=col, sticky='ew', padx=1, pady=1)
        
        # H.Level(%) row
        tk.Label(table_frame, text="H.Level(%)", font=('Arial', 8), bg='#d4d0c8', anchor='w').grid(row=1, column=0, sticky='w', padx=2)
        h_level_values = ["0", "0", "0", "0", "0", "0", "0", "0", "0"]
        self.h_level_entries = []
        for col, val in enumerate(h_level_values):
            entry = tk.Entry(table_frame, width=8, font=('Arial', 8))
            entry.insert(0, val)
            entry.grid(row=1, column=col+1, padx=1, pady=1)
            self.h_level_entries.append(entry)
        
        # L.Level(%) row
        tk.Label(table_frame, text="L.Level(%)", font=('Arial', 8), bg='#d4d0c8', anchor='w').grid(row=2, column=0, sticky='w', padx=2)
        l_level_values = ["20", "20", "0", "0", "0", "0", "0", "0", "0"]
        self.l_level_entries = []
        for col, val in enumerate(l_level_values):
            entry = tk.Entry(table_frame, width=8, font=('Arial', 8))
            entry.insert(0, val) 
            entry.grid(row=2, column=col+1, padx=1, pady=1)
            self.l_level_entries.append(entry)
        
        # S2.Detail button
        detail_btn_frame = tk.Frame(level_inner, bg='#d4d0c8')
        detail_btn_frame.pack(fill=tk.X, pady=5)
        
        s2_detail_btn = tk.Button(
            detail_btn_frame,
            text="S2.Detail",
            command=self.on_s2_detail_clicked,
            width=12,
            font=('Arial', 9),
            bg='#d4d0c8',
            relief=tk.RAISED,
            bd=2
        )
        s2_detail_btn.pack(side=tk.LEFT, padx=5)
        
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
        
        pre_btn = tk.Button(left_buttons, text="8.Pre.", command=self.on_pre_clicked, **button_config)
        pre_btn.pack(side=tk.LEFT, padx=3)
        
        print_btn = tk.Button(left_buttons, text="4.Print", command=self.on_print_clicked, **button_config)
        print_btn.pack(side=tk.LEFT, padx=3)
        
        # Upload button (NEW)
        upload_btn = tk.Button(left_buttons, text="Upload", command=self.on_upload_clicked, **button_config)
        upload_btn.pack(side=tk.LEFT, padx=3)
        
        # Right side button
        right_buttons = tk.Frame(button_frame, bg='#d4d0c8')
        right_buttons.pack(side=tk.RIGHT)
        
        cancel_btn = tk.Button(right_buttons, text="9.Cancel", command=self.on_cancel_clicked, **button_config)
        cancel_btn.pack(side=tk.RIGHT, padx=3)
    
    def on_monitor_ele_changed(self, event=None):
        """Update monitor value when element is changed"""
        selected_ele = self.monitor_ele.get()
        if selected_ele in self.monitor_ele_values:
            self.monitor_value.delete(0, tk.END)
            self.monitor_value.insert(0, self.monitor_ele_values[selected_ele])
    
    def collect_form_data(self):
        """Collect all form data into a unified JSON format"""
        form_data = {
            "analytical_group": self.selected_group,
            "analytical_method": self.analytical_method.get(),
            "seq": {
                "purge": {
                    "seq1": self.purge_seq1.get()
                },
                "source": {
                    "seq1": self.source_seq1.get(),
                    "seq2": self.source_seq2.get(),
                    "seq3": self.source_seq3.get(),
                    "clean": self.source_clean.get()
                },
                "preburn": {
                    "seq1": self.preburn_seq1.get(),
                    "seq2": self.preburn_seq2.get(),
                    "seq3": self.preburn_seq3.get(),
                    "clean": "Pulse"
                },
                "integ": {
                    "seq1": self.integ_seq1.get(),
                    "seq2": self.integ_seq2.get(),
                    "seq3": self.integ_seq3.get(),
                    "clean": "Pulse"
                },
                "clean": {
                    "value": self.clean_entry.get(),
                    "unit": "Pulse"
                }
            },
            "level_out_information": {
                "monitor_element": {
                    "element": self.monitor_ele.get(),
                    "value": self.monitor_value.get(),
                    "option1": self.monitor_none1.get(),
                    "option2": self.monitor_none2.get()
                },
                "h_level_percent": [entry.get() for entry in self.h_level_entries],
                "l_level_percent": [entry.get() for entry in self.l_level_entries]
            }
        }
        return form_data
    
    def load_saved_data(self):
        """Load previously saved data if exists"""
        saved_data = self.data_manager.get_analytical_condition()
        if not saved_data:
            return
        
        try:
            # Load analytical method
            if 'analytical_method' in saved_data:
                self.analytical_method.set(saved_data['analytical_method'])
            
            # Load SEQ data
            if 'seq' in saved_data:
                seq = saved_data['seq']
                
                # Purge
                if 'purge' in seq and 'seq1' in seq['purge']:
                    self.purge_seq1.delete(0, tk.END)
                    self.purge_seq1.insert(0, seq['purge']['seq1'])
                
                # Source
                if 'source' in seq:
                    if 'seq1' in seq['source']:
                        self.source_seq1.set(seq['source']['seq1'])
                    if 'seq2' in seq['source']:
                        self.source_seq2.set(seq['source']['seq2'])
                    if 'seq3' in seq['source']:
                        self.source_seq3.set(seq['source']['seq3'])
                    if 'clean' in seq['source']:
                        self.source_clean.set(seq['source']['clean'])
                
                # Preburn
                if 'preburn' in seq:
                    if 'seq1' in seq['preburn']:
                        self.preburn_seq1.delete(0, tk.END)
                        self.preburn_seq1.insert(0, seq['preburn']['seq1'])
                    if 'seq2' in seq['preburn']:
                        self.preburn_seq2.delete(0, tk.END)
                        self.preburn_seq2.insert(0, seq['preburn']['seq2'])
                    if 'seq3' in seq['preburn']:
                        self.preburn_seq3.delete(0, tk.END)
                        self.preburn_seq3.insert(0, seq['preburn']['seq3'])
                
                # Integ
                if 'integ' in seq:
                    if 'seq1' in seq['integ']:
                        self.integ_seq1.delete(0, tk.END)
                        self.integ_seq1.insert(0, seq['integ']['seq1'])
                    if 'seq2' in seq['integ']:
                        self.integ_seq2.delete(0, tk.END)
                        self.integ_seq2.insert(0, seq['integ']['seq2'])
                    if 'seq3' in seq['integ']:
                        self.integ_seq3.delete(0, tk.END)
                        self.integ_seq3.insert(0, seq['integ']['seq3'])
                
                # Clean
                if 'clean' in seq and 'value' in seq['clean']:
                    self.clean_entry.delete(0, tk.END)
                    self.clean_entry.insert(0, seq['clean']['value'])
            
            # Load Level Out Information
            if 'level_out_information' in saved_data:
                level_info = saved_data['level_out_information']
                
                # Monitor element
                if 'monitor_element' in level_info:
                    mon_ele = level_info['monitor_element']
                    if 'element' in mon_ele:
                        self.monitor_ele.set(mon_ele['element'])
                    if 'value' in mon_ele:
                        self.monitor_value.delete(0, tk.END)
                        self.monitor_value.insert(0, mon_ele['value'])
                    if 'option1' in mon_ele:
                        self.monitor_none1.set(mon_ele['option1'])
                    if 'option2' in mon_ele:
                        self.monitor_none2.set(mon_ele['option2'])
                
                # H Level
                if 'h_level_percent' in level_info:
                    for idx, value in enumerate(level_info['h_level_percent']):
                        if idx < len(self.h_level_entries):
                            self.h_level_entries[idx].delete(0, tk.END)
                            self.h_level_entries[idx].insert(0, value)
                
                # L Level
                if 'l_level_percent' in level_info:
                    for idx, value in enumerate(level_info['l_level_percent']):
                        if idx < len(self.l_level_entries):
                            self.l_level_entries[idx].delete(0, tk.END)
                            self.l_level_entries[idx].insert(0, value)
        
        except Exception as e:
            print(f"Error loading saved data: {e}")
    
    def save_current_data(self):
        """Save current form data before leaving page"""
        form_data = self.collect_form_data()
        self.data_manager.save_analytical_condition(form_data)
    
    def on_upload_clicked(self):
        """Handler for Upload button - Uploads data to backend API"""
        try:
            # Collect all form data
            form_data = self.collect_form_data()
            
            # Convert to JSON for display
            json_data = json.dumps(form_data, indent=2)
            
            # Display the JSON that will be sent
            print("\n" + "="*50)
            print("ANALYTICAL CONDITION - UPLOADING TO BACKEND:")
            print("="*50)
            print(json_data)
            print("="*50 + "\n")
            
            # Upload to backend API
            response = self.data_manager.upload_analytical_condition(form_data)
            
            # Show success message with API response
            if response and 'records' in response:
                created_record = response['records'][0]
                record_id = created_record.get('id', 'N/A')
                messagebox.showinfo(
                    "Upload Successful",
                    f"Analytical Condition uploaded successfully!\n\n"
                    f"Record ID: {record_id}\n"
                    f"Analytical Group: {self.selected_group}\n"
                    f"Method: {form_data.get('analytical_method', 'N/A')}\n\n"
                    f"Data saved to database."
                )
            else:
                messagebox.showinfo(
                    "Upload Complete",
                    "Data uploaded successfully!"
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
        messagebox.showinfo("OK", "Settings saved successfully!")
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
    
    def on_next_clicked(self):
        """Handler for Next button - Navigate to next page"""
        self.save_current_data()
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        # Open Attenuator Information page
        AttenuatorInformationPage(self.parent_frame, self.selected_group, self)
    
    def on_pre_clicked(self):
        """Handler for Pre. button - Go back to previous page"""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
    
    def on_print_clicked(self):
        """Handler for Print button"""
        messagebox.showinfo("Print", "Printing analytical conditions...")
    
    def on_cancel_clicked(self):
        """Handler for Cancel button"""
        confirm = messagebox.askyesno("Cancel", "Are you sure you want to cancel? Changes will not be saved.")
        if confirm:
            for widget in self.parent_frame.winfo_children():
                widget.destroy()
    
    def on_s2_detail_clicked(self):
        """Handler for S2.Detail button"""
        messagebox.showinfo("S2 Detail", "Opening S2 Detail window...")
