import tkinter as tk
from tkinter import ttk, messagebox
import json, os
from utils.data_manager import DataManager


PI_OPTIONS = ["P:PDA Mode", "I:Integ.Mode"]
METHOD_OPTIONS = [
    "0:Integration",
    "2:Distribution",
    "6:Metarographic",
    "9:Interval integration",
    "A:To Get Sampling Count",
    "I:Input For DCA"
]
AREA_OPTIONS = [
    "T:Total Area",
    "S:Spark Area",
    "A:Arc Area"
]


class MeasurementModePage:
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
        path = os.path.join(os.path.dirname(__file__),
                            "../examples/measurement_mode.json")
        with open(path, "r") as f:
            self.data = json.load(f)

    def create_widgets(self):
        title = tk.Label(self.frame, text=f"Measurement Mode - {self.selected_group}",
                        font=("Arial",10,"bold"), bg="#5c9bd5", fg="white", anchor="w")
        title.pack(fill=tk.X)

        self.table_frame = tk.Frame(self.frame, bg="#d4d0c8")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        headers = ["Ele.Name","P/I","Method","M","N","I","Area"]
        for c,h in enumerate(headers):
            tk.Label(self.table_frame, text=h, font=("Arial",9,"bold"),
                    bg="#d4d0c8", width=15, relief=tk.RIDGE)\
                .grid(row=0, column=c, sticky="nsew")

        self.rows = []

        for r, row in enumerate(self.data["measurements"], start=1):

            tk.Label(self.table_frame, text=row["element"], bg="white", width=15, relief=tk.SUNKEN)\
                .grid(row=r, column=0)

            pi = ttk.Combobox(self.table_frame, values=PI_OPTIONS, width=14, state="readonly")
            pi.set(row["P/I"])
            pi.grid(row=r, column=1)

            method = ttk.Combobox(self.table_frame, values=METHOD_OPTIONS, width=18, state="readonly")
            method.set(row["method"])
            method.grid(row=r, column=2)

            m = tk.Entry(self.table_frame, width=6)
            m.insert(0, row["M"])
            m.grid(row=r, column=3)

            n = tk.Entry(self.table_frame, width=6)
            n.insert(0, row["N"])
            n.grid(row=r, column=4)

            i = tk.Entry(self.table_frame, width=6)
            i.insert(0, row["I"])
            i.grid(row=r, column=5)

            area = ttk.Combobox(self.table_frame, values=AREA_OPTIONS, width=14, state="readonly")
            area.set(row["area"])
            area.grid(row=r, column=6)

            self.rows.append((pi, method, m, n, i, area))

        # Buttons
        btn_frame = tk.Frame(self.frame, bg="#d4d0c8")
        btn_frame.pack(fill=tk.X, pady=6)

        cfg = dict(width=10, font=("Arial",9), bg="#d4d0c8", relief=tk.RAISED, bd=2)

        tk.Button(btn_frame, text="1.OK", command=self.on_ok, **cfg).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="2.Next", command=self.on_next, **cfg).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="8.Pre.", command=self.on_pre, **cfg).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="4.Print", command=self.on_print, **cfg).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="9.Cancel", command=self.on_cancel, **cfg).pack(side=tk.RIGHT, padx=3)


    def collect_data(self):
        data = []
        for idx,(pi,method,m,n,i,area) in enumerate(self.rows):
            data.append({
                "element": self.data["measurements"][idx]["element"],
                "P/I": pi.get(),
                "method": method.get(),
                "M": m.get(),
                "N": n.get(),
                "I": i.get(),
                "area": area.get()
            })
        return {"analytical_group": self.selected_group, "measurements": data}


    def on_ok(self):
        self.data_manager.save_measurement_mode(self.collect_data())
        messagebox.showinfo("Saved","Measurement Mode saved")
        self.clear()

    def on_next(self):
        self.data_manager.save_measurement_mode(self.collect_data())
        self.clear()
        messagebox.showinfo("Next","Proceed to next page")

    def on_pre(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        from pages.channel_information import ChannelInformationPage
        ChannelInformationPage(self.parent_frame, self.selected_group, self.parent_app)


    def on_print(self):
        messagebox.showinfo("Print","Printing Measurement Mode")

    def on_cancel(self):
        if messagebox.askyesno("Cancel","Discard changes?"):
            self.clear()

    def clear(self):
        for w in self.parent_frame.winfo_children():
            w.destroy()
