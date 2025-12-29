import tkinter as tk
from tkinter import ttk, messagebox
from pages.filing_mode import FilingModeDialog
from pages.transmission_mode import TransmissionModeDialog
from utils.data_manager import DataManager

class AnalyticalModePage:
    def __init__(self, parent_frame, selected_group, parent_app=None):
        self.parent_frame = parent_frame
        self.selected_group = selected_group
        self.parent_app = parent_app
        self.data_manager = DataManager()

        self.frame = tk.Frame(parent_frame, bg="#d4d0c8")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.frame, text=f"Analytical Mode - {self.selected_group}",
                         font=("Arial",10,"bold"), bg="#5c9bd5", fg="white", anchor="w")
        title.pack(fill=tk.X)

        top = tk.Frame(self.frame, bg="#d4d0c8")
        top.pack(fill=tk.X, padx=10, pady=4)

        tk.Label(top, text="Common", bg="#d4d0c8").pack(side=tk.LEFT)
        self.common_entry = tk.Entry(top, width=15)
        self.common_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="8:Refer.", width=8).pack(side=tk.LEFT, padx=5)

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.cont_tab = tk.Frame(self.notebook, bg="#d4d0c8")
        self.int_tab  = tk.Frame(self.notebook, bg="#d4d0c8")
        self.recal_tab= tk.Frame(self.notebook, bg="#d4d0c8")

        self.notebook.add(self.cont_tab, text="Cont.")
        self.notebook.add(self.int_tab, text="Int.")
        self.notebook.add(self.recal_tab,text="Recal.")

        self.build_common(self.cont_tab, "cont")
        self.build_common(self.int_tab,  "int")
        self.build_common(self.recal_tab,"recal")

        self.build_bottom_buttons()

    def build_common(self, frame, mode):
        f1 = tk.Frame(frame, bg="#d4d0c8")
        f1.pack(anchor="w", padx=10, pady=5)

        tk.Label(f1,text="Number of Analysis",bg="#d4d0c8").grid(row=0,column=0,sticky="w")
        tk.Spinbox(f1,from_=1,to=9,width=5).grid(row=0,column=1)

        if mode=="cont":
            g = tk.LabelFrame(f1,text="Analysis method",bg="#d4d0c8")
            g.grid(row=1,column=0,columnspan=2,pady=5,sticky="w")
            v=tk.StringVar(value="4")
            tk.Radiobutton(g,text="Normal",variable=v,value="1",bg="#d4d0c8").pack(anchor="w")
            tk.Radiobutton(g,text="4-times analysis",variable=v,value="4",bg="#d4d0c8").pack(anchor="w")

        if mode=="recal":
            g = tk.LabelFrame(f1,text="Recal. Method",bg="#d4d0c8")
            g.grid(row=1,column=0,columnspan=2,pady=5,sticky="w")
            v=tk.StringVar(value="2")
            tk.Radiobutton(g,text="1 point Recal.",variable=v,value="1",bg="#d4d0c8").pack(anchor="w")
            tk.Radiobutton(g,text="2 point Recal.",variable=v,value="2",bg="#d4d0c8").pack(anchor="w")

        layout = tk.LabelFrame(frame,text="Display Layout",bg="#d4d0c8")
        layout.pack(anchor="ne", padx=20, pady=5)

        for i,(t) in enumerate(["Row of Ele.","Col. of EachResult","Magn."]):
            tk.Label(layout,text=t,bg="#d4d0c8").grid(row=i,column=0,sticky="w")
            tk.Entry(layout,width=6).grid(row=i,column=1)

        d = tk.LabelFrame(frame,text="Display item",bg="#d4d0c8")
        d.pack(side=tk.LEFT,padx=10)
        for t in ["R value","S.D.","C.V."]:
            tk.Checkbutton(d,text=t,bg="#d4d0c8").pack(anchor="w")

        p = tk.LabelFrame(frame,text="Print item",bg="#d4d0c8")
        p.pack(side=tk.LEFT,padx=10)
        for t in ["Each Result","R value","S.D.","C.V."]:
            tk.Checkbutton(p,text=t,bg="#d4d0c8").pack(anchor="w")
        tk.Button(p,text="7:Detail",width=8).pack(pady=3)

        pm = tk.LabelFrame(frame,text="Print mode",bg="#d4d0c8")
        pm.pack(side=tk.LEFT,padx=10)
        v=tk.StringVar(value="Manu")
        tk.Radiobutton(pm,text="Auto",variable=v,value="Auto",bg="#d4d0c8").pack(anchor="w")
        tk.Radiobutton(pm,text="Manu",variable=v,value="Manu",bg="#d4d0c8").pack(anchor="w")

        if mode=="cont":
            tk.Button(frame,text="5:FileMode",width=10,command=self.open_filing_mode).pack(side=tk.RIGHT,padx=10)
            tk.Button(frame,text="6:Trans.Mode",width=10,command=self.open_transmission_mode).pack(side=tk.RIGHT,padx=10)
            
        if mode == "cont":
            sample = tk.LabelFrame(frame, text="SampleIndex", bg="#d4d0c8")
            sample.pack(fill=tk.X, padx=15, pady=6)

            self.sample_index_1 = tk.Entry(sample, width=40)
            self.sample_index_1.insert(0, "E 415:2021 / JIS G 1253:2002 / IS 8811:1998 (RA 2018)")
            self.sample_index_1.pack(padx=5, pady=3)

            self.sample_index_2 = tk.Entry(sample, width=40)
            self.sample_index_2.insert(0, "[Sk-23-5212-P]")
            self.sample_index_2.pack(padx=5, pady=3)

    def build_bottom_buttons(self):
        btns=tk.Frame(self.frame,bg="#d4d0c8")
        btns.pack(fill=tk.X,pady=6)

        cfg=dict(width=10,bg="#d4d0c8",relief=tk.RAISED,bd=2)

        tk.Button(btns,text="1.OK",command=self.on_ok,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="2.Next",command=self.on_next,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="3.Pre.",command=self.on_pre,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="S2.Cont.",command=lambda: self.notebook.select(self.cont_tab),**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="S3.Int.",command=lambda: self.notebook.select(self.int_tab),**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="S4.Recal.",command=lambda: self.notebook.select(self.recal_tab),**cfg).pack(side=tk.LEFT,padx=3)

        tk.Button(btns,text="4.Print",command=self.on_print,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="9.Cancel",command=self.on_cancel,**cfg).pack(side=tk.RIGHT,padx=3)


    def collect_data(self):
        data = {
            "analytical_group": self.selected_group,
            "common": self.common_entry.get(),
            "sample_index": {
                "line1": self.sample_index_1.get() if hasattr(self, "sample_index_1") else "",
                "line2": self.sample_index_2.get() if hasattr(self, "sample_index_2") else ""
            },
            "tabs": {}
        }

        for name, tab in [("cont", self.cont_tab), ("int", self.int_tab), ("recal", self.recal_tab)]:
            tab_data = {}

            for child in tab.winfo_children():
                if isinstance(child, tk.LabelFrame):

                    if child.cget("text") == "Display Layout":
                        entries = child.winfo_children()
                        tab_data["display_layout"] = {
                            "row_of_ele": entries[1].get(),
                            "col_each_result": entries[3].get(),
                            "magn": entries[5].get()
                        }

                    if child.cget("text") == "Display item":
                        tab_data["display_item"] = [
                            cb.cget("text") for cb in child.winfo_children()
                            if isinstance(cb, tk.Checkbutton)
                        ]

                    if child.cget("text") == "Print item":
                        tab_data["print_item"] = [
                            cb.cget("text") for cb in child.winfo_children()
                            if isinstance(cb, tk.Checkbutton)
                        ]

                    if child.cget("text") == "Print mode":
                        for rb in child.winfo_children():
                            if isinstance(rb, tk.Radiobutton):
                                tab_data["print_mode"] = rb.cget("value")

                    if child.cget("text") in ("Analysis method", "Recal. Method"):
                        for rb in child.winfo_children():
                            if isinstance(rb, tk.Radiobutton):
                                tab_data["analysis_method"] = rb.cget("value")

            data["tabs"][name] = tab_data

        return data

    def open_filing_mode(self):
        FilingModeDialog(self.frame)

    def open_transmission_mode(self):
        TransmissionModeDialog(self.frame)
    def on_ok(self):
        self.data_manager.save_analytical_mode(self.collect_data())
        self.clear()

    def on_next(self):
        self.data_manager.save_analytical_mode(self.collect_data())

        for w in self.parent_frame.winfo_children():
            w.destroy()
        from pages.control_chart_information import ControlChartInformationPage
        ControlChartInformationPage(self.parent_frame, self.selected_group, self.parent_app)



    def on_pre(self):
        self.clear()
        from pages.master_curve_information import MasterCurveInformationPage
        MasterCurveInformationPage(self.parent_frame, self.selected_group, self.parent_app)

    def on_print(self):
        messagebox.showinfo("Print","Printing Analytical Mode")


    def on_cancel(self):
        if messagebox.askyesno("Cancel","Discard changes?"):
            self.clear()

    def clear(self):
        for w in self.parent_frame.winfo_children():
            w.destroy()