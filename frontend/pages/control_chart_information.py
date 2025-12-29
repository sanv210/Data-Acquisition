import tkinter as tk
from tkinter import ttk, messagebox
import json, os


class ControlChartInformationPage:
    def __init__(self, parent_frame, selected_group, parent_app=None):
        self.parent_frame = parent_frame
        self.selected_group = selected_group
        self.parent_app = parent_app

        self.frame = tk.Frame(parent_frame, bg="#d4d0c8")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.load_json()
        self.create_widgets()

    def load_json(self):
        path = os.path.join(os.path.dirname(__file__), "../examples/control_chart_information.json")
        with open(path, "r") as f:
            self.data = json.load(f)["control_chart_information"]

    def create_widgets(self):
        title = tk.Label(self.frame, text=f"Control Chart Information - {self.selected_group}",
                         font=("Arial", 10, "bold"), bg="#5c9bd5", fg="white", anchor="w")
        title.pack(fill=tk.X)

        # ================== OPTIONS ==================
        opt = tk.Frame(self.frame, bg="#d4d0c8")
        opt.pack(fill=tk.X, padx=10, pady=5)

        self.ctrl_line = tk.IntVar(value=1)
        self.sigma_line = tk.IntVar(value=1)

        tk.Checkbutton(opt, text="Control Line", variable=self.ctrl_line, bg="#d4d0c8").grid(row=0, column=0, sticky="w")
        tk.Checkbutton(opt, text="Sigma Line", variable=self.sigma_line, bg="#d4d0c8").grid(row=0, column=2, sticky="w")

        self.range_type = tk.StringVar(value="standard")
        tk.Radiobutton(opt, text="Standard Range", variable=self.range_type, value="standard", bg="#d4d0c8").grid(row=1, column=0, sticky="w")
        tk.Radiobutton(opt, text="Control Range", variable=self.range_type, value="control", bg="#d4d0c8").grid(row=2, column=0, sticky="w")

        self.sigma_type = tk.StringVar(value="2")
        tk.Radiobutton(opt, text="±1.0STD", variable=self.sigma_type, value="1", bg="#d4d0c8").grid(row=1, column=2, sticky="w")
        tk.Radiobutton(opt, text="±2.0STD", variable=self.sigma_type, value="2", bg="#d4d0c8").grid(row=2, column=2, sticky="w")
        tk.Radiobutton(opt, text="±1.5STD", variable=self.sigma_type, value="1.5", bg="#d4d0c8").grid(row=1, column=3, sticky="w")
        tk.Radiobutton(opt, text="±3.0STD", variable=self.sigma_type, value="3", bg="#d4d0c8").grid(row=2, column=3, sticky="w")

        # Center line
        center = tk.LabelFrame(opt, text="Center line", bg="#d4d0c8")
        center.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.center_type = tk.StringVar(value="avg")
        tk.Radiobutton(center, text="Average", variable=self.center_type, value="avg", bg="#d4d0c8").pack(anchor="w")
        tk.Radiobutton(center, text="Median", variable=self.center_type, value="med", bg="#d4d0c8").pack(anchor="w")
        tk.Radiobutton(center, text="Target", variable=self.center_type, value="tar", bg="#d4d0c8").pack(anchor="w")

        tk.Label(opt, text="Class Mark", bg="#d4d0c8").grid(row=3, column=2, sticky="e")
        self.class_mark = tk.Entry(opt, width=6)
        self.class_mark.insert(0, "1")
        self.class_mark.grid(row=3, column=3)

        scale = tk.LabelFrame(opt, text="Display Scale", bg="#d4d0c8")
        scale.grid(row=4, column=2, columnspan=2, padx=5, pady=5)
        self.scale_type = tk.StringVar(value="auto")
        tk.Radiobutton(scale, text="Auto", variable=self.scale_type, value="auto", bg="#d4d0c8").pack(anchor="w")
        tk.Radiobutton(scale, text="Fixed", variable=self.scale_type, value="fixed", bg="#d4d0c8").pack(anchor="w")

        # ================== TABLE ==================
        table_frame = tk.Frame(self.frame, bg="#d4d0c8")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        canvas = tk.Canvas(table_frame)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        scroll = tk.Frame(canvas)

        scroll.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        headers = ["Ele.Name", "Target", "L", "H", "L", "H"]
        for c, h in enumerate(headers):
            tk.Label(scroll, text=h, bg="#e0e0e0", width=12, relief=tk.RIDGE).grid(row=0, column=c)

        self.rows = []

        for r, row in enumerate(self.data, start=1):
            tk.Label(scroll, text=row["element"], bg="white", relief=tk.SUNKEN, width=12).grid(row=r, column=0)
            t = tk.Entry(scroll, width=12); t.insert(0, row["target"]); t.grid(row=r, column=1)
            cl = tk.Entry(scroll, width=12); cl.insert(0, row["control_range"]["L"]); cl.grid(row=r, column=2)
            ch = tk.Entry(scroll, width=12); ch.insert(0, row["control_range"]["H"]); ch.grid(row=r, column=3)
            sl = tk.Entry(scroll, width=12); sl.insert(0, row["scale_range"]["L"]); sl.grid(row=r, column=4)
            sh = tk.Entry(scroll, width=12); sh.insert(0, row["scale_range"]["H"]); sh.grid(row=r, column=5)

            self.rows.append((row["element"], t, cl, ch, sl, sh))

        # ================== BUTTONS ==================
        btns = tk.Frame(self.frame, bg="#d4d0c8")
        btns.pack(fill=tk.X, pady=6)

        cfg = dict(width=10, bg="#d4d0c8", relief=tk.RAISED, bd=2)
        tk.Button(btns, text="1:OK", command=self.on_ok, **cfg).pack(side=tk.LEFT, padx=3)
        tk.Button(btns, text="2:Next", command=self.on_ok, **cfg).pack(side=tk.LEFT, padx=3)
        tk.Button(btns, text="3:Pre.", **cfg).pack(side=tk.LEFT, padx=3)
        tk.Button(btns, text="4:Print", **cfg).pack(side=tk.LEFT, padx=3)
        tk.Button(btns, text="9:Cancel", command=self.clear, **cfg).pack(side=tk.RIGHT, padx=3)

    def on_ok(self):
        messagebox.showinfo("Saved", "Control Chart Information Saved")
        self.clear()

    def clear(self):
        for w in self.parent_frame.winfo_children():
            w.destroy()

    def on_next(self):
        self.on_ok()

    def on_pre(self):
        self.clear()
        from pages.analytical_mode import AnalyticalModePage
        AnalyticalModePage(self.parent_frame, self.selected_group, self.parent_app)