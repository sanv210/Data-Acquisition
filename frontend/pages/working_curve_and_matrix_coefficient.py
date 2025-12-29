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
        self.current_index = 0

        self.frame = tk.Frame(parent_frame, bg="#d4d0c8")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.load_json()
        self.create_widgets()
        self.load_element_data()

    def load_json(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../examples/working_curve_and_matrix_coefficient.json")
        with open(path, "r") as f:
            self.data = json.load(f)["working_curve_and_matrix_coefficient"]

    def create_widgets(self):
        tk.Label(self.frame, text=f"Working Curve and Matrix coefficient - {self.selected_group}",
                 font=("Arial",10,"bold"), bg="#5c9bd5", fg="white", anchor="w").pack(fill=tk.X)

        main = tk.Frame(self.frame, bg="#d4d0c8")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # -------- LEFT ELEMENT LIST ----------
        left = tk.Frame(main, bg="white", relief=tk.SUNKEN, bd=2)
        left.pack(side=tk.LEFT, fill=tk.Y)

        self.listbox = tk.Listbox(left, width=10)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        for ele in self.data:
            self.listbox.insert(tk.END, ele["element"]+"1")

        self.listbox.selection_set(0)
        self.listbox.bind("<<ListboxSelect>>", self.on_element_select)

        # -------- RIGHT PANEL ----------
        right = tk.Frame(main, bg="#d4d0c8", relief=tk.SUNKEN, bd=2)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        self.fields = {}

        def f(lbl,r,c,w=10):
            tk.Label(right,text=lbl,bg="#d4d0c8").grid(row=r,column=c,sticky="e",padx=4,pady=2)
            e=tk.Entry(right,width=w)
            e.grid(row=r,column=c+1,padx=4,pady=2)
            return e

        tk.Label(right,text="Working Curve",font=("Arial",9,"bold"),bg="#d4d0c8").grid(row=0,column=0,sticky="w")

        self.fields["divide"]=f("Divide",1,0)
        self.fields["no"]=f("No.",1,2)

        self.fields["range_h"]=f("Range",2,0)
        tk.Label(right,text="-",bg="#d4d0c8").grid(row=2,column=2)
        self.fields["range_l"]=f("",2,2)

        self.fields["unit"]=f("Unit",3,0)
        self.fields["order"]=f("Order",3,2)
        self.fields["std"]=f("STD.",4,0,15)

        # Coefficients a b c d
        tk.Label(right,text="a").grid(row=6,column=1)
        tk.Label(right,text="b").grid(row=6,column=3)
        tk.Label(right,text="c").grid(row=6,column=5)
        tk.Label(right,text="d").grid(row=6,column=7)

        self.fields["a"]=tk.Entry(right,width=10); self.fields["a"].grid(row=7,column=1)
        self.fields["b"]=tk.Entry(right,width=10); self.fields["b"].grid(row=7,column=3)
        self.fields["c"]=tk.Entry(right,width=10); self.fields["c"].grid(row=7,column=5)
        self.fields["d"]=tk.Entry(right,width=10); self.fields["d"].grid(row=7,column=7)

        # ---------- MATRIX COEFFICIENT ----------
        tk.Label(right,text="Matrix Coefficient",font=("Arial",9,"bold"),bg="#d4d0c8")\
            .grid(row=8,column=0,sticky="w",pady=5)

        self.matrix_entries=[]
        for side in [0,1]:
            base = 9
            for i in range(9):
                r=base+i
                e1=tk.Entry(right,width=4); e1.grid(row=r,column=side*6)
                e2=tk.Entry(right,width=6); e2.grid(row=r,column=side*6+1)
                e3=tk.Entry(right,width=10); e3.grid(row=r,column=side*6+2)
                self.matrix_entries.append((e1,e2,e3))

        # ---------- BUTTONS ----------
        btn=tk.Frame(self.frame,bg="#d4d0c8")
        btn.pack(fill=tk.X,pady=6)

        cfg=dict(width=10,bg="#d4d0c8",relief=tk.RAISED,bd=2)
        tk.Button(btn,text="1:OK",command=self.on_ok,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btn,text="2:Next",command=self.on_next,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btn,text="3:Pre.",command=self.on_pre,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btn,text="4:Print",**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btn,text="9:Cancel",command=self.on_cancel,**cfg).pack(side=tk.RIGHT,padx=3)

    def load_element_data(self):
        d=self.data[self.current_index]
        wc=d["working_curve"]

        self.fields["divide"].delete(0,tk.END); self.fields["divide"].insert(0,wc["divide"])
        self.fields["no"].delete(0,tk.END); self.fields["no"].insert(0,wc["no"])
        self.fields["range_h"].delete(0,tk.END); self.fields["range_h"].insert(0,wc["range"]["h"])
        self.fields["range_l"].delete(0,tk.END); self.fields["range_l"].insert(0,wc["range"]["l"])
        self.fields["unit"].delete(0,tk.END); self.fields["unit"].insert(0,wc["unit"])
        self.fields["order"].delete(0,tk.END); self.fields["order"].insert(0,wc["order"])
        self.fields["std"].delete(0,tk.END); self.fields["std"].insert(0,wc["std"])

        for k in ["a","b","c","d"]:
            self.fields[k].delete(0,tk.END)
            self.fields[k].insert(0,wc["coefficient"][k])

        for (e1,e2,e3),m in zip(self.matrix_entries,d["matrix_coefficient"]):
            e1.delete(0,tk.END); e1.insert(0,m["D/L"])
            e2.delete(0,tk.END); e2.insert(0,m["element"])
            e3.delete(0,tk.END); e3.insert(0,m["coefficient"])

    def on_element_select(self,e=None):
        s=self.listbox.curselection()
        if s:
            self.current_index=s[0]
            self.load_element_data()

    def on_ok(self):
        messagebox.showinfo("Saved","Working curve saved")

    def on_next(self):
        if self.current_index<len(self.data)-1:
            self.current_index+=1
            self.listbox.selection_clear(0,tk.END)
            self.listbox.selection_set(self.current_index)
            self.load_element_data()

    def on_pre(self):
        if self.current_index>0:
            self.current_index-=1
            self.listbox.selection_clear(0,tk.END)
            self.listbox.selection_set(self.current_index)
            self.load_element_data()

    def on_cancel(self):
        for w in self.parent_frame.winfo_children():
            w.destroy()
