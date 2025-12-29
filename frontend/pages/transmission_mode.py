import tkinter as tk

class TransmissionModeDialog:
    def __init__(self,parent):
        self.win = tk.Toplevel(parent)
        self.win.title("Transmission Mode")
        self.win.geometry("350x230")
        self.win.configure(bg="#d4d0c8")
        self.win.grab_set()

        mode = tk.LabelFrame(self.win, text="Mode", bg="#d4d0c8")
        mode.pack(side=tk.LEFT, padx=15, pady=20)

        self.mode_var = tk.StringVar(value="Manu")
        tk.Radiobutton(mode,text="Auto",variable=self.mode_var,value="Auto",bg="#d4d0c8").pack(anchor="w")
        tk.Radiobutton(mode,text="Manu",variable=self.mode_var,value="Manu",bg="#d4d0c8").pack(anchor="w")

        trans_item = tk.LabelFrame(self.win, text="Trans. item", bg="#d4d0c8")
        trans_item.pack(side=tk.LEFT, padx=10, pady=20)

        self.items = {}
        for t in ["Each Result","Average","Intensity","Round Ave."]:
            v=tk.BooleanVar()
            tk.Checkbutton(trans_item,text=t,variable=v,bg="#d4d0c8").pack(anchor="w")
            self.items[t]=v

        b=tk.Frame(self.win,bg="#d4d0c8")
        b.pack(fill=tk.X,pady=5)

        tk.Button(b,text="1:OK",width=10,command=self.win.destroy).pack(side=tk.LEFT,padx=10)
        tk.Button(b,text="9:Cancel",width=10,command=self.win.destroy).pack(side=tk.RIGHT,padx=10)
