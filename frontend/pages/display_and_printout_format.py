import tkinter as tk
from tkinter import ttk, messagebox
import json, os
from utils.data_manager import DataManager


class DisplayAndPrintoutFormatPage:
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
        path = os.path.join(os.path.dirname(__file__), "../examples/display_and_printout_format.json")
        with open(path,"r") as f:
            data=json.load(f)
        self.disp_data=data["display_and_printout_format"]
        self.trans_data=data["trans"]

    def create_widgets(self):
        title=tk.Label(self.frame,text=f"Display and Printout Format - {self.selected_group}",
                       font=("Arial",10,"bold"),bg="#5c9bd5",fg="white",anchor="w")
        title.pack(fill=tk.X)

        tab_frame=tk.Frame(self.frame,bg="#d4d0c8")
        tab_frame.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)

        self.tabs=ttk.Notebook(tab_frame)
        self.tabs.pack(fill=tk.BOTH,expand=True)

        self.disp_tab=self.build_table_tab(self.disp_data)
        self.trans_tab=self.build_table_tab(self.trans_data)

        self.tabs.add(self.disp_tab,text="Disp. and Print")
        self.tabs.add(self.trans_tab,text="Trans.")

        btns=tk.Frame(self.frame,bg="#d4d0c8")
        btns.pack(fill=tk.X,pady=6)

        cfg=dict(width=10,bg="#d4d0c8",relief=tk.RAISED,bd=2)

        tk.Button(btns,text="1.OK",command=self.on_ok,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="2.Next",command=self.on_next,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="3.Pre.",command=self.on_pre,**cfg).pack(side=tk.LEFT,padx=3)
        
        tk.Button(btns,text="S2:D/P",command=lambda:self.tabs.select(0),**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="S3:Trans.",command=lambda:self.tabs.select(1),**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="4.Print",command=self.on_print,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="9.Cancel",command=self.on_cancel,**cfg).pack(side=tk.RIGHT,padx=3)

    def build_table_tab(self,data):
        frame=tk.Frame(self.tabs,bg="#d4d0c8")

        canvas=tk.Canvas(frame,bg="white",highlightthickness=0)
        scroll=ttk.Scrollbar(frame,orient="vertical",command=canvas.yview)
        inner=tk.Frame(canvas,bg="white")

        inner.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0),window=inner,anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        scroll.pack(side=tk.RIGHT,fill=tk.Y)

        headers=["Ele.Name","Order","Magn.","Int.","Deci."]
        for c,h in enumerate(headers):
            tk.Label(inner,text=h,bg="#e0e0e0",relief=tk.RIDGE,width=12)\
                .grid(row=0,column=c)

        rows=[]
        for r,row in enumerate(data,start=1):
            tk.Label(inner,text=row["element"],bg="white",relief=tk.SUNKEN,width=12)\
                .grid(row=r,column=0)

            e1=tk.Entry(inner,width=12); e1.insert(0,row["order"]); e1.grid(row=r,column=1)
            e2=tk.Entry(inner,width=12); e2.insert(0,row["magn"]);  e2.grid(row=r,column=2)
            e3=tk.Entry(inner,width=12); e3.insert(0,row["int"]);   e3.grid(row=r,column=3)
            e4=tk.Entry(inner,width=12); e4.insert(0,row["deci"]); e4.grid(row=r,column=4)

            rows.append((row["element"],e1,e2,e3,e4))

        frame.rows=rows
        return frame

    def collect_tab_data(self,tab):
        return [
            {"element":e,"order":o.get(),"magn":m.get(),"int":i.get(),"deci":d.get()}
            for e,o,m,i,d in tab.rows
        ]

    def on_ok(self):
        data={
            "analytical_group":self.selected_group,
            "display_and_printout_format":self.collect_tab_data(self.disp_tab),
            "trans":self.collect_tab_data(self.trans_tab)
        }
        self.data_manager.save_display_and_printout_format(data)
        messagebox.showinfo("Saved","Display & Print Format saved")
        self.clear()

    def on_next(self):
        self.clear()
        from pages.master_curve_information import MasterCurveInformationPage
        MasterCurveInformationPage(self.parent_frame, self.selected_group, self.parent_app)

    def on_pre(self):
        self.clear()
        from pages.standard_information import StandardInformationPage
        StandardInformationPage(self.parent_frame, self.selected_group, self.parent_app)

    def on_print(self):
        messagebox.showinfo("Print","Printing Display Format")

    def on_cancel(self):
        if messagebox.askyesno("Cancel","Discard changes?"):
            self.clear()

    def clear(self):
        for w in self.parent_frame.winfo_children():
            w.destroy()
