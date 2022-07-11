from guiFramework import *
from listTemplates import FiberList, LaminaList
from formTemplates import NewLaminaForm, NewFiberForm, AlterFiberForm
from db_sqlite3_v3 import DbHandler
import sys

class Header(tk.Menu):
    def __init__(self, parentWidget:tk.Widget, *, dbHandler:DbHandler = None):
        tk.Menu.__init__(self, parentWidget)

        self._parent = parentWidget

        menu_file = tk.Menu(self, tearoff=0)
        menu_file.add_command(label="Export...", underline=1, command=lambda:print("Export all data as csv"))
        menu_file.add_command(label="Exit", underline=1, command=self.quit)
        self.add_cascade(label="File", underline=0, menu=menu_file)

        menu_create = tk.Menu(self, tearoff=0)
        menu_create.add_command(label="Fiber", underline=1, command=lambda:NewFiberForm(self._parent, "Add new fiber", dbHandler=dbHandler))
        menu_create.add_command(label="Lamina", underline=1, command=lambda:NewLaminaForm(self._parent, "Add new lamina", dbHandler=dbHandler))
        self.add_cascade(label="Create", underline=0, menu=menu_create)
        
        menu_list = tk.Menu(self, tearoff=0)
        menu_list.add_command(label="Fiber", underline=1, command=lambda:FiberList(self._parent, "Available fibers", dbHandler=dbHandler))
        menu_list.add_command(label="Lamina", underline=1, command=lambda:LaminaList(self._parent, "Available laminas", dbHandler=dbHandler))
        self.add_cascade(label="Lists", underline=0, menu=menu_list)

    def quit(self):
        sys.exit(0)


class MainPage(App):
    def __init__(self, title:str, *, width:int = 600, height:int = 400, posx:int = 300, posy:int = 100):
        super().__init__(title, width=width, height=height, posx=posx, posy=posy)
        
        ## Defining header menu
        self._dbHandler = DbHandler("laminateBase.db")
        self._header = Header(self._root, dbHandler=self._dbHandler)
        self._root.config(menu=self._header)
        self.startApp()


gui = MainPage("Testapp")