import tkinter as tk
from formTemplates import NewFiberForm
from listTemplates import FiberList, LaminaList

# low-level functions
def startApp(title:str, *, width:int = 600, height:int = 400, posx:int = 300, posy:int = 100):
    root = tk.Tk()
    root.title(title)
    root.geometry(f"{width}x{height}+{posx}+{posy}")
    try:
        root.iconbitmap("./.assets/grid.ico")
    except:
        print("No icon will be displayed")
    msg = tk.Label(root, text="Title").grid(column=0,row=0)
    return root

def createWindow(parentWidget, title:str, *, dynamicSize:bool = False, width:int = 600, height:int = 400, posx:int = 400, posy:int = 150):
    """Creates new window for app

    :param parentWidget:    parent widget of window
    :param str title:       widow title
    :param int width:       width of window (default 600px)
    :param int height:      height of window (dafault 400px)      
    :param int posx:        horisontal position of window on screen (default 400px)
    :param int posy:        vertical position of window on screen (default 150px)
    :return:                window object
    """
    newWin = tk.Toplevel(parentWidget)
    newWin.title(title)
    if not dynamicSize:
        newWin.geometry(f"{width}x{height}+{posx}+{posy}")
    try:
        newWin.iconbitmap(".assets/grid.ico")
    except:
        print("No logo will be displayed")
    return newWin

def createTable(parentWidget,*, titles:list):
    """Custom basefunction for creating tables of data
     
     :param parentWidget:   parent widget of the table
     :param list titles:    list containing titles for table
     :return:               table object 
    """
    table = tk.Frame(parentWidget)
    for i,title in enumerate(titles):
        tk.Label(table,text=title).grid(column=i, row=0)
    return table



# creation of lists:

def laminaDetailedList(parentWidget):
    """Creates table object for a detailed list of laminas using the createTable function
    
    :param parentWidget:    parent widget of the table
    :return:                table object
    """
    headers = ["ID", "Fiber type", "Name", "Fabric", "Usecase", "FAW", "E1", "E2", "G12", "Nu", "Thickness", "Comment"]
    laminaTable = createTable(parentWidget, titles=headers)
    return laminaTable

def laminaInfoList(parentWidget):
    """Creates table object for listing lamina info using the createTable function 
    
    :param parentWidget:    parent widget of the table
    :return:                table object
    """
    headers = ["ID", "Name", "FAW", "Usecase"]
    laminaTable = createTable(parentWidget, titles=headers)

def fiberList(partentWidget):
    """Creates table for listing fiber data using the createTable function
    
    :param parentWidget:    parent widget of the table
    :return:                table object
    """
    headers = ["ID", "Fiber type", "Name", "E (GPa)", "UTS (GPa)", "Density", "Comment"]
    testset = [{"id":1, "fiberType":"Carbon", "name":"test1", "youngs":210, "uts":3.83, "rho":2.12, "comment":"No comment"},
            {"id":2, "fiberType":"Aramid", "name":"test2", "youngs":220, "uts":4.83, "rho":3.12, "comment":"No comment"},
            {"id":3, "fiberType":"Glass", "name":"test3", "youngs":230, "uts":5.83, "rho":4.12, "comment":"No comment"}]
    fiberTable = createTable(partentWidget, titles=headers)
    for i, fiber in enumerate(testset):
        for j,key in enumerate(fiber):
            tk.Label(fiberTable, text = fiber[key]).grid(column = j, row=i+1)
    return fiberTable

def dummyFunc(parentWidget):
    """dummy function for buttons. Creates new window with a dummy button w/ no commands attached to it
    
    :param parentWidget:    parent widget of the new window
    :return:                window object
    """
    filewin = createWindow(parentWidget, "Dummy window")
    button = tk.Button(filewin, text = "Do nothing button",command=lambda:dummyFunc(filewin))
    button.pack()


# widow creation

def window_laminaSelection(parentWidget) -> tk.Widget:
    win = createWindow(parentWidget, "Lamina Selection")
    
    title = tk.Label(win, text="Hello world", justify=tk.CENTER)
    title.grid(column=0,row=0)
    
    return win


def window_fibers() -> tk.Widget:
    pass

# TEST CODE

def main() -> None:
    """Creates a test GUI for handling of data"""
    gui = startApp("Test GUI")
    table = fiberList(gui)
    table.grid(column=0, row=1)

    header_menubar = tk.Menu(gui)

    header_createmenu = tk.Menu(header_menubar, tearoff=0)
    header_createmenu.add_command(label = "Fiber", command=lambda:NewFiberForm(gui, "Add new fiber"))
    header_createmenu.add_command(label="Lamina", command=lambda:print("Not an option yet"))
    
    header_listmenu = tk.Menu(header_menubar, tearoff=0)
    header_listmenu.add_command(label="Fiber", command=lambda:FiberList(gui, "Available fibers"))
    header_listmenu.add_command(label="Lamina", command=lambda:LaminaList(gui, "Available laminas"))

    header_menubar.add_cascade(label="Create", menu=header_createmenu)
    header_menubar.add_cascade(label="List", menu=header_listmenu)
    gui.config(menu=header_menubar)
    gui.mainloop()

if __name__ == "__main__":
    main()