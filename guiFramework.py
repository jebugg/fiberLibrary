import tkinter as tk

from db_sqlite3_v3 import DbHandler

class App:
    def __init__(self, title:str, *, width:int = 600, height:int = 400, posx:int = 300, posy:int = 100):
        self._root = tk.Tk()
        
        self._root.title(title)
        self._root.geometry(f"{width}x{height}+{posx}+{posy}")

        try:
            self._root.iconbitmap("./.assets/grid.ico")
        except:
            print("No icon will be displayed")
        
        self._msg = tk.Label(self._root, text = "Title").grid(column=0, row=0)
    
    def startApp(self):
        self._root.mainloop()

class SubWindow:
    def __init__(self, parentWidget:tk.Widget, /, title:str, *, dbHandler:DbHandler = None, dynamicSize:bool = False, width:int = 600, height:int = 400, posx:int = 400, posy:int = 150):
        self._parent = parentWidget
        self._win = tk.Toplevel(self._parent)

        self._dbConn = dbHandler
        if not dynamicSize:
            self._win.geometry(f"{width}x{height}+{posx}+{posy}")
        
        self._win.title(title)

    def close(self):
        self._win.destroy()