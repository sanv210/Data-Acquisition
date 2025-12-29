import tkinter as tk
from tkinter import ttk, messagebox
import json, os
from utils.data_manager import DataManager


class Correction100Page:
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
        path = os.path.join(os.path.dirname(__file__), "../examples/100_correction.json")
        with open(path, "r") as f:
            self.data = json.load(f)["100_correction"]

    def create_widgets(self):
        title = tk.Label(self.frame, text=f"100% Correction - {self.selected_group}",
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

        tk.Label(scroll_frame,text="Ele.Name",bg="#e0e0e0",relief=tk.RIDGE,width=18).grid(row=0,column=0)
        tk.Label(scroll_frame,text="Y / N / I",bg="#e0e0e0",relief=tk.RIDGE,width=10).grid(row=0,column=1)

        self.rows = []

        for r, row in enumerate(self.data, start=1):
            tk.Label(scroll_frame,text=row["element"],bg="white",relief=tk.SUNKEN,width=18)\
                .grid(row=r,column=0,sticky="nsew")
            cb = ttk.Combobox(scroll_frame, values=["Y","N","I"], width=7, state="readonly")
            cb.set(row["Y/N/I"])
            cb.grid(row=r,column=1)
            self.rows.append((row["element"],cb))

        note = tk.Label(self.frame,
            text="Y : Require 100% correction     N : Not require 100% correction     I : Base Element\nSpace is same meaning of 'I'.",
            bg="#d4d0c8", anchor="w", font=("Arial",8))
        note.pack(fill=tk.X, padx=10)

        btns = tk.Frame(self.frame, bg="#d4d0c8")
        btns.pack(fill=tk.X, pady=6)

        cfg=dict(width=10,bg="#d4d0c8",relief=tk.RAISED,bd=2)

        tk.Button(btns,text="1.OK",command=self.on_ok,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="2.Next",command=self.on_next,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="3.Pre.",command=self.on_pre,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="4.Print",command=self.on_print,**cfg).pack(side=tk.LEFT,padx=3)
        tk.Button(btns,text="9.Cancel",command=self.on_cancel,**cfg).pack(side=tk.RIGHT,padx=3)

    def collect_data(self):
        return {
            "analytical_group": self.selected_group,
            "100_correction":[{"element":e,"Y/N/I":cb.get()} for e,cb in self.rows]
        }

    def on_ok(self):
        self.data_manager.save_100_correction(self.collect_data())
        messagebox.showinfo("Saved","100% Correction saved")
        self.clear()

    def on_next(self):
        self.data_manager.save_100_correction(self.collect_data())
        self.clear()
        from pages.standard_information import StandardInformationPage
        StandardInformationPage(self.parent_frame, self.selected_group, self.parent_app)

    def on_pre(self):
        self.clear()
        from pages.measurement_mode import RecalibrationInformationPage
        RecalibrationInformationPage(self.parent_frame, self.selected_group, self.parent_app)

    def on_print(self):
        messagebox.showinfo("Print","Printing 100% Correction")

    def on_cancel(self):
        if messagebox.askyesno("Cancel","Discard changes?"):
            self.clear()

    def clear(self):
        for w in self.parent_frame.winfo_children():
            w.destroy()