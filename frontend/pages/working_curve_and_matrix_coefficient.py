import tkinter as tk
from tkinter import ttk, messagebox
import json, os
from utils.data_manager import DataManager


class WorkingCurveMatrixPage:
    def __init__(self, parent_frame, selected_group, parent_app=None):
        self.parent_frame = parent_frame
        self.selected_group = selected_group
        self.parent_app = parent_app
        self.data_manager = DataManager()

        self.frame = tk.Frame(parent_frame, bg="#d4d0c8")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.load_json()
        self.current_index = 0

        self.create_widgets()
        self.load_element_data()

    # -------------------- LOAD DATA --------------------

    def load_json(self):
        path = os.path.join(os.path.dirname(__file__), "../examples/working_curve_and_matrix_coefficient.json")
        with open(path, "r") as f:
            self.data = json.load(f)["working_curve_and_matrix_coefficient"]

    # -------------------- UI --------------------

    def create_widgets(self):
        title = tk.Label(self.frame, text=f"Working Curve and Matrix coefficient - {self.selected_group}",
                         font=("Arial",10,"bold"), bg="#5c9bd5", fg="white", anchor="w")
        title.pack(fill=tk.X)

        main = tk.Frame(self.frame, bg="#d4d0c8")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # -------- LEFT LIST --------
        left = tk.Frame(main, bg="white", relief=tk.SUNKEN, bd=2)
        left.pack(side=tk.LEFT, fill=tk.Y)

        self.listbox = tk.Listbox(left, width=12)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        for ele in self.data:
            self.listbox.insert(tk.END, ele["element"]+"1")

        self.listbox.selection_set(0)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # -------- RIGHT PANEL --------
        right = tk.Frame(main, bg="#d4d0c8")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        self.build_working_curve(right)
        self.build_matrix_coefficient(right)
        self.build_buttons()

    # ---------------- WORKING CURVE -----------------

    def build_working_curve(self, parent):
        box = tk.LabelFrame(parent, text="Working Curve", bg="#d4d0c8")
        box.pack(fill=tk.X, padx=10, pady=6)

        self.fields = {}

        def field(lbl, r, c, w=10):
            tk.Label(box,text=lbl,bg="#d4d0c8").grid(row=r,column=c,sticky="e",padx=6,pady=3)
            e=tk.Entry(box,width=w)
            e.grid(row=r,column=c+1,sticky="w",padx=6,pady=3)
            return e

        self.fields["divide"]=field("Divide",0,0,6)
        self.fields["no"]=field("No.",0,4,6)

        self.fields["range_h"]=field("Range",1,0,8)
        tk.Label(box,text="-",bg="#d4d0c8").grid(row=1,column=2)
        self.fields["range_l"]=tk.Entry(box,width=8)
        self.fields["range_l"].grid(row=1,column=3)

        self.fields["unit"]=field("Unit",2,0,6)
        self.fields["order"]=field("Order",2,4,6)
        self.fields["std"]=field("STD.",3,0,14)

        for i,t in enumerate(["a","b","c","d"]):
            tk.Label(box,text=t,bg="#d4d0c8").grid(row=4,column=1+i*2)
            self.fields[t]=tk.Entry(box,width=10)
            self.fields[t].grid(row=5,column=1+i*2)

    # ---------------- MATRIX COEFFICIENT -----------------

    def build_matrix_coefficient(self, parent):
        box = tk.LabelFrame(parent,text="Matrix Coefficient",bg="#d4d0c8")
        box.pack(fill=tk.X,padx=10,pady=6)

        self.matrix_entries=[]

        for col in range(2):
            base=col*6
            tk.Label(box,text="D/L",bg="#d4d0c8").grid(row=0,column=base)
            tk.Label(box,text="Ele.Name",bg="#d4d0c8").grid(row=0,column=base+1)
            tk.Label(box,text="Coefficient",bg="#d4d0c8").grid(row=0,column=base+2)

            for i in range(8):
                r=i+1
                e1=tk.Entry(box,width=4)
                e2=tk.Entry(box,width=6)
                e3=tk.Entry(box,width=10)
                e1.grid(row=r,column=base)
                e2.grid(row=r,column=base+1)
                e3.grid(row=r,column=base+2)
                self.matrix_entries.append((e1,e2,e3))

    # ---------------- BUTTONS -----------------

    def build_buttons(self):
        b=tk.Frame(self.frame,bg="#d4d0c8")
        b.pack(fill=tk.X,pady=6)

        cfg=dict(width=10,bg="#d4d0c8",relief=tk.RAISED,bd=2)

        tk.Button(b,text="1:OK",command=self.on_ok,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(b,text="2:Next",command=self.on_next,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(b,text="3:Pre",command=self.on_pre,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(b,text="4:Next Ele.",command=self.next_ele,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(b,text="5:Pre.Ele.",command=self.prev_ele,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(b,text="6:Print",command=lambda:messagebox.showinfo("Print","Printing"),**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(b,text="9:Cancel",command=self.on_cancel,**cfg).pack(side=tk.RIGHT,padx=3)

    # ---------------- DATA BINDING -----------------

    def load_element_data(self):
        wc=self.data[self.current_index]["working_curve"]

        self.fields["divide"].delete(0,'end'); self.fields["divide"].insert(0,wc["divide"])
        self.fields["no"].delete(0,'end'); self.fields["no"].insert(0,wc["no."])
        self.fields["range_h"].delete(0,'end'); self.fields["range_h"].insert(0,wc["range"]["h"])
        self.fields["range_l"].delete(0,'end'); self.fields["range_l"].insert(0,wc["range"]["l"])
        self.fields["unit"].delete(0,'end'); self.fields["unit"].insert(0,wc["unit"])
        self.fields["order"].delete(0,'end'); self.fields["order"].insert(0,wc["order"])
        self.fields["std"].delete(0,'end'); self.fields["std"].insert(0,wc["std"])

        for k in ["a","b","c","d"]:
            self.fields[k].delete(0,'end')
            self.fields[k].insert(0,wc["coefficient"][k])
            
            
        matrix = self.data[self.current_index]["matrix_coefficient"]
        
        for i, row in enumerate(matrix):
            if i >= len(self.matrix_entries):
                break

            e1, e2, e3 = self.matrix_entries[i]
            e1.delete(0, 'end')
            e2.delete(0, 'end')
            e3.delete(0, 'end')

            e1.insert(0, row["D/L"])
            e2.insert(0, row["element"])
            e3.insert(0, row["coefficient"])

    def collect_data(self):
        wc = {
            "divide": self.fields["divide"].get(),
            "no.": self.fields["no"].get(),
            "range": {
                "h": self.fields["range_h"].get(),
                "l": self.fields["range_l"].get()
            },
            "unit": self.fields["unit"].get(),
            "order": self.fields["order"].get(),
            "std": self.fields["std"].get(),
            "coefficient": {
                "a": self.fields["a"].get(),
                "b": self.fields["b"].get(),
                "c": self.fields["c"].get(),
                "d": self.fields["d"].get()
            }
        }

        matrix = []
        for e1, e2, e3 in self.matrix_entries:
            matrix.append({
                "D/L": e1.get(),
                "element": e2.get(),
                "coefficient": e3.get()
            })

        self.data[self.current_index]["working_curve"] = wc
        self.data[self.current_index]["matrix_coefficient"] = matrix

        return {
            "analytical_group": self.selected_group,
            "working_curve_and_matrix_coefficient": self.data
        }

    def on_select(self,e):
        self.current_index=self.listbox.curselection()[0]
        self.load_element_data()

    def next_ele(self):
        if self.current_index<len(self.data)-1:
            self.current_index+=1
            self.listbox.selection_clear(0,'end')
            self.listbox.selection_set(self.current_index)
            self.load_element_data()

    def prev_ele(self):
        if self.current_index>0:
            self.current_index-=1
            self.listbox.selection_clear(0,'end')
            self.listbox.selection_set(self.current_index)
            self.load_element_data()

    def on_ok(self):
        self.data_manager.save_working_curve(self.collect_data())
        messagebox.showinfo("Saved","Working Curve Saved")


    def on_cancel(self):
        for w in self.parent_frame.winfo_children():
            w.destroy()
    def on_next(self):
        self.data_manager.save_working_curve(self.collect_data())
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        from pages.correction import Correction100Page
        Correction100Page(self.parent_frame, self.selected_group, self.parent_app)
    def on_pre(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        from pages.recalibration_information import RecalibrationInformationPage
        RecalibrationInformationPage(self.parent_frame, self.selected_group, self.parent_app)
