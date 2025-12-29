import tkinter as tk
from tkinter import ttk, messagebox
import json, os
from utils.data_manager import DataManager


class MasterCurveInformationPage:
    def __init__(self, parent_frame, selected_group, parent_app=None):
        self.parent_frame = parent_frame
        self.selected_group = selected_group
        self.parent_app = parent_app
        self.data_manager = DataManager()

        self.frame = tk.Frame(self.parent_frame, bg="#d4d0c8")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.load_json()
        self.create_widgets()

    def load_json(self):
        path = os.path.join(os.path.dirname(__file__), "../examples/master_curve_information.json")
        with open(path,"r") as f:
            self.data = json.load(f)["master_curve_information"]

    def create_widgets(self):
        title = tk.Label(self.frame, text=f"Master Curve Information - {self.selected_group}",
                         font=("Arial",10,"bold"), bg="#5c9bd5", fg="white", anchor="w")
        title.pack(fill=tk.X)

        container = tk.Frame(self.frame, bg="#d4d0c8")
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        headers=["Ele.Name","M.C.Sample","Target","D1","D2","AC","MC","Flag"]
        for c,h in enumerate(headers):
            tk.Label(scroll_frame,text=h,bg="#e0e0e0",relief=tk.RIDGE,width=14)\
                .grid(row=0,column=c)

        self.rows=[]

        for r,row in enumerate(self.data,start=1):
            tk.Label(scroll_frame,text=row["element"],bg="white",relief=tk.SUNKEN,width=14)\
                .grid(row=r,column=0)

            e1=tk.Entry(scroll_frame,width=14); e1.insert(0,row["m.c.sample"]); e1.grid(row=r,column=1)
            e2=tk.Entry(scroll_frame,width=14); e2.insert(0,row["target"]);     e2.grid(row=r,column=2)
            e3=tk.Entry(scroll_frame,width=14); e3.insert(0,row["D1"]);         e3.grid(row=r,column=3)
            e4=tk.Entry(scroll_frame,width=14); e4.insert(0,row["D2"]);         e4.grid(row=r,column=4)
            e5=tk.Entry(scroll_frame,width=14); e5.insert(0,row["AC"]);         e5.grid(row=r,column=5)
            e6=tk.Entry(scroll_frame,width=14); e6.insert(0,row["MC"]);         e6.grid(row=r,column=6)
            e7=tk.Entry(scroll_frame,width=14); e7.insert(0,row["flag"]);       e7.grid(row=r,column=7)

            self.rows.append((row["element"],e1,e2,e3,e4,e5,e6,e7))

        btns=tk.Frame(self.frame,bg="#d4d0c8")
        btns.pack(fill=tk.X,pady=6)

        cfg=dict(width=10,bg="#d4d0c8",relief=tk.RAISED,bd=2)

        tk.Button(btns,text="1.OK",command=self.on_ok,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="2.Next",command=self.on_next,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="3.Pre.",command=self.on_pre,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="4.Print",command=self.on_print,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="7.Init.",command=self.on_init,**cfg).pack(side=tk.RIGHT,padx=3)
        tk.Button(btns,text="9.Cancel",command=self.on_cancel,**cfg).pack(side=tk.RIGHT,padx=3)

    def collect_data(self):
        return {
            "analytical_group":self.selected_group,
            "master_curve_information":[
                {
                    "element":e,
                    "m.c.sample":s.get(),
                    "target":t.get(),
                    "D1":d1.get(),
                    "D2":d2.get(),
                    "AC":ac.get(),
                    "MC":mc.get(),
                    "flag":f.get()
                }
                for e,s,t,d1,d2,ac,mc,f in self.rows
            ]
        }

    def on_ok(self):
        self.data_manager.save_master_curve_information(self.collect_data())
        self.clear()

    def on_next(self):
        self.on_ok()
        from pages.analytical_mode import AnalyticalModePage
        AnalyticalModePage(self.parent_frame, self.selected_group, self.parent_app)

    def on_pre(self):
        self.clear()
        from pages.display_and_printout_format import DisplayAndPrintoutFormatPage
        DisplayAndPrintoutFormatPage(self.parent_frame, self.selected_group, self.parent_app)

    def on_print(self):
        messagebox.showinfo("Print","Printing Master Curve")

    def on_init(self):
        messagebox.askyesno("Initialize","Initialize Coefficients, OK?")


    def on_cancel(self):
        if messagebox.askyesno("Cancel","Discard changes?"):
            self.clear()

    def clear(self):
        for w in self.parent_frame.winfo_children():
            w.destroy()
