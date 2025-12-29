import tkinter as tk
from tkinter import ttk, messagebox
import json, os
from utils.data_manager import DataManager

class RecalibrationInformationPage:
    def __init__(self, parent_frame, selected_group, parent_app=None):
        self.parent_frame = parent_frame
        self.selected_group = selected_group
        self.parent_app = parent_app
        self.data_manager = DataManager()

        self.frame = tk.Frame(self.parent_frame, bg="#d4d0c8")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.load_json()
        self.current_index = 0

        self.create_widgets()
        self.load_element_data()

    def load_json(self):
        path = os.path.join(os.path.dirname(__file__), "../examples/recalibration_information.json")
        with open(path, "r") as f:
            self.data = json.load(f)["recalibration"]

    def create_widgets(self):
        title = tk.Label(self.frame, text=f"Recalibration Information - {self.selected_group}",
                         font=("Arial",10,"bold"), bg="#5c9bd5", fg="white", anchor="w")
        title.pack(fill=tk.X)

        main = tk.Frame(self.frame, bg="#d4d0c8")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left = tk.Frame(main, bg="white", width=120, relief=tk.SUNKEN, bd=2)
        left.pack(side=tk.LEFT, fill=tk.Y)

        self.listbox = tk.Listbox(left, width=12)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        for ele in self.data:
            self.listbox.insert(tk.END, ele["element"]+"1")

        self.listbox.selection_set(0)
        self.listbox.bind("<<ListboxSelect>>", self.on_element_select)

        right = tk.Frame(main, bg="#d4d0c8", relief=tk.SUNKEN, bd=2)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        self.entries = {}

        def field(lbl,row,col):
            tk.Label(right,text=lbl,bg="#d4d0c8").grid(row=row,column=col*2,sticky="e",padx=4,pady=2)
            e=tk.Entry(right,width=12)
            e.grid(row=row,column=col*2+1,padx=4,pady=2)
            return e

        tk.Label(right,text="High").grid(row=0,column=1)
        tk.Label(right,text="Low").grid(row=0,column=3)
        tk.Label(right,text="K").grid(row=0,column=5)

        self.entries["snH"]=field("Sample Name",1,0)
        self.entries["snL"]=field("",1,1)
        self.entries["snK"]=field("",1,2)

        self.entries["tH"]=field("Target",2,0)
        self.entries["tL"]=field("",2,1)
        self.entries["tK"]=field("",2,2)

        self.entries["rH"]=field("Range",3,0)
        self.entries["rL"]=field("",3,1)
        self.entries["rK"]=field("",3,2)

        tk.Label(right, text="coefficient", bg="#d4d0c8", font=("Arial",9,"bold"))\
            .grid(row=5, column=0, sticky="e", padx=5, pady=8)

        tk.Label(right, text="Alpha", bg="#d4d0c8").grid(row=4, column=1)
        tk.Label(right, text="Beta",  bg="#d4d0c8").grid(row=4, column=3)
        tk.Label(right, text="K",     bg="#d4d0c8").grid(row=4, column=5)

        self.entries["a"] = tk.Entry(right, width=12)
        self.entries["a"].grid(row=5, column=1, padx=4, pady=2)

        self.entries["b"] = tk.Entry(right, width=12)
        self.entries["b"].grid(row=5, column=3, padx=4, pady=2)

        self.entries["k"] = tk.Entry(right, width=12)
        self.entries["k"].grid(row=5, column=5, padx=4, pady=2)


        btns = tk.Frame(self.frame,bg="#d4d0c8")
        btns.pack(fill=tk.X)

        cfg=dict(width=10,bg="#d4d0c8",relief=tk.RAISED,bd=2)


        tk.Button(btns,text="1.OK",command=self.on_ok,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns, text="2.Next", command=self.on_next, **cfg).pack(side=tk.LEFT, padx=3)
        tk.Button(btns,text="S2:N.Ele",command=self.next_element,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="S3:P.Ele",command=self.prev_element,**cfg).pack(side=tk.LEFT,padx=3)        
        tk.Button(btns, text="s5:Init.", command=self.on_init, **cfg).pack(side=tk.LEFT, padx=3)
        tk.Button(btns, text="8.Pre.", command=self.on_pre, **cfg).pack(side=tk.LEFT, padx=3)
        tk.Button(btns,text="9.Cancel",command=self.on_cancel,**cfg).pack(side=tk.RIGHT,padx=3)

    def load_element_data(self):
        info = self.data[self.current_index]["recalibration_info"]

        self.entries["snH"].delete(0,tk.END); self.entries["snH"].insert(0,info["sample_name"]["High"])
        self.entries["snL"].delete(0,tk.END); self.entries["snL"].insert(0,info["sample_name"]["Low"])
        self.entries["snK"].delete(0,tk.END); self.entries["snK"].insert(0,info["sample_name"]["K"])

        self.entries["tH"].delete(0,tk.END); self.entries["tH"].insert(0,info["target"]["High"])
        self.entries["tL"].delete(0,tk.END); self.entries["tL"].insert(0,info["target"]["Low"])
        self.entries["tK"].delete(0,tk.END); self.entries["tK"].insert(0,info["target"]["K"])

        self.entries["rH"].delete(0,tk.END); self.entries["rH"].insert(0,info["range"]["High"])
        self.entries["rL"].delete(0,tk.END); self.entries["rL"].insert(0,info["range"]["Low"])
        self.entries["rK"].delete(0,tk.END); self.entries["rK"].insert(0,info["range"]["K"])

        self.entries["a"].delete(0,tk.END); self.entries["a"].insert(0,info["coefficient"]["Alpha"])
        self.entries["b"].delete(0,tk.END); self.entries["b"].insert(0,info["coefficient"]["Beta"])
        self.entries["k"].delete(0,tk.END); self.entries["k"].insert(0,info["coefficient"]["K"])

    def collect_data(self):
        result = []

        for idx, ele in enumerate(self.data):
            info = ele["recalibration_info"]

            if idx == self.current_index:
                info = {
                    "sample_name": {
                        "High": self.entries["snH"].get(),
                        "Low": self.entries["snL"].get(),
                        "K": self.entries["snK"].get()
                    },
                    "target": {
                        "High": self.entries["tH"].get(),
                        "Low": self.entries["tL"].get(),
                        "K": self.entries["tK"].get()
                    },
                    "range": {
                        "High": self.entries["rH"].get(),
                        "Low": self.entries["rL"].get(),
                        "K": self.entries["rK"].get()
                    },
                    "coefficient": {
                        "Alpha": self.entries["a"].get(),
                        "Beta": self.entries["b"].get(),
                        "K": self.entries["k"].get()
                    }
                }

            result.append({
                "element": ele["element"],
                "recalibration_info": info
            })

        return {
            "analytical_group": self.selected_group,
            "recalibration": result
        }

    def next_element(self):
        if self.current_index < len(self.data)-1:
            self.current_index +=1
            self.listbox.selection_clear(0,tk.END)
            self.listbox.selection_set(self.current_index)
            self.load_element_data()

    def prev_element(self):
        if self.current_index >0:
            self.current_index -=1
            self.listbox.selection_clear(0,tk.END)
            self.listbox.selection_set(self.current_index)
            self.load_element_data()

    def on_element_select(self,e=None):
        sel=self.listbox.curselection()
        if sel:
            self.current_index=sel[0]
            self.load_element_data()

    def on_ok(self):
        messagebox.showinfo("Saved","Recalibration data saved")
        for w in self.parent_frame.winfo_children():
            w.destroy()
    def on_next(self):
        self.data_manager.save_measurement_mode(self.collect_data())
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        from pages.working_curve_and_matrix_coefficient import WorkingCurveMatrixPage    
        WorkingCurveMatrixPage(self.parent_frame, self.selected_group, self.parent_app)

    def on_pre(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        from pages.measurement_mode import MeasurementModePage
        MeasurementModePage(self.parent_frame, self.selected_group, self.parent_app)
        
    def on_cancel(self):
        for w in self.parent_frame.winfo_children():
            w.destroy() 
            
    def on_init(self):
        messagebox.askyesno("Initialize","Initialize coefficients. OK?")