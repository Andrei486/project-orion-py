import tkinter as tk

class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(self, parent, *args, **kwargs)
        self.parent = parent
    
    def load_army(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    Application(root).pack(side="top", fill="both", expand=True)
    root.mainloop()