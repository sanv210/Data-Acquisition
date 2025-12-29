import tkinter as tk

class FilingModeDialog:
    def __init__(self,parent):
        self.win=tk.Toplevel(parent)
        self.win.title("Filing Mode")
        self.win.geometry("350x220")
        self.win.configure(bg="#d4d0c8")
        self.win.grab_set()

        mode=tk.LabelFrame(self.win,text="Mode",bg="#d4d0c8")
        mode.pack(side=tk.LEFT,padx=15,pady=20)

        v=tk.StringVar(value="Manu")
        tk.Radiobutton(mode,text="Auto",variable=v,value="Auto",bg="#d4d0c8").pack(anchor="w")
        tk.Radiobutton(mode,text="Manu",variable=v,value="Manu",bg="#d4d0c8").pack(anchor="w")

        fileitem=tk.LabelFrame(self.win,text="File item",bg="#d4d0c8")
        fileitem.pack(side=tk.LEFT,padx=10,pady=20)

        for t in ["Each Result","Average","Intensity","Round Ave."]:
            tk.Checkbutton(fileitem,text=t,bg="#d4d0c8").pack(anchor="w")

        b=tk.Frame(self.win,bg="#d4d0c8")
        b.pack(fill=tk.X,pady=5)

        tk.Button(b,text="1:OK",width=10,command=self.win.destroy).pack(side=tk.LEFT,padx=10)
        tk.Button(b,text="9:Cancel",width=10,command=self.win.destroy).pack(side=tk.RIGHT,padx=10)
