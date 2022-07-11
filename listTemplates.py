from guiFramework import *
from formTemplates import NewFiberForm, NewLaminaForm
class DataList(SubWindow):
    def __init__(self, parentWidget:tk.Widget, /, title:str, *, dbHandler:DbHandler = None, dynamicSize:bool = True, width:int = 600, height:int = 400, posx:int = 400, posy:int = 150):
        super().__init__(parentWidget, title, dbHandler=dbHandler, dynamicSize=dynamicSize, width=width, height=height, posx=posx, posy=posy)
        self._rowNumHeader = 0
        self._rowNumList = 1
        self._rowNumBtns = 2
        self._deleteBtnState = False

        self._numRowsPerPage = 5
        self._currPage = 1

        self._listFrame  = tk.Frame(self._win)
        self._navBtnsFrame = tk.Frame(self._win)
        self._editBtnsFrame = tk.Frame(self._win)

        self._retrieveData()

        self._btn_next = tk.Button(self._navBtnsFrame, text = "Next", command=self.nextPage)
        self._btn_prev = tk.Button(self._navBtnsFrame, text = "Previous", command=self.prevPage)
        self._btn_cancel = tk.Button(self._navBtnsFrame, text = "Cancel", command=self.close)
        
        self._btn_add = tk.Button(self._editBtnsFrame, text = "Add", command=self.addInstance)
        self._btn_refresh = tk.Button(self._editBtnsFrame, text = "Refresh", command=self._refresh)

        self._btn_prev.grid(column=0, row=0)
        self._btn_cancel.grid(column=1, row=0)
        self._btn_next.grid(column=2, row=0)

        self._btn_add.grid(column=0, row=0)
        self._btn_refresh.grid(column=1, row=0)
        self._listFrame.grid(column=0, columnspan = 4, row=self._rowNumList)
        self._navBtnsFrame.grid(column=0, columnspan = 4, row=self._rowNumBtns, sticky=tk.W)
        self._editBtnsFrame.grid(column=4, row=self._rowNumBtns, sticky=tk.E)
        
        self._win.grid_rowconfigure(1, weight=1)

        self._updatePage()


    def drawTable(self):
        for item in self._listFrame.winfo_children():
            item.destroy()
        for i,title in enumerate(self._titles):
            tk.Label(self._listFrame, text=str(title).upper()).grid(column=i, row=0, sticky=tk.W)

        for i in range((self._currPage-1)*self._numRowsPerPage, min(self._currPage*self._numRowsPerPage, len(self._data))):
            for j,key in enumerate(self._data[i]):
                e = tk.Label(self._listFrame, text=self._data[i][key])
                if j == 0:
                    e.grid(column=j, row=i%self._numRowsPerPage+1, sticky=tk.E)
                else:
                    e.grid(column=j, row=i%self._numRowsPerPage+1, sticky=tk.W)
        self._listFrame.grid(column=0, columnspan=4, row=0, sticky=tk.W)
    def _refresh(self):
        self._retrieveData()
        self._updatePage()

    def _updatePage(self):
        if self._currPage >= int(len(self._data)/self._numRowsPerPage) + int(len(self._data)%self._numRowsPerPage != 0):
            self._btn_next["state"] = tk.DISABLED
        else:
            self._btn_next["state"] = tk.NORMAL
        
        if self._currPage < 2:
            self._btn_prev["state"] = tk.DISABLED
        else:
            self._btn_prev["state"] = tk.NORMAL
        
        self.drawTable()
    
    def nextPage(self):
        if self._currPage <= int(len(self._data)/self._numRowsPerPage):
            self._currPage += 1
        self._updatePage()

    def prevPage(self):
        if self._currPage > 1:
            self._currPage -= 1
        self._updatePage()
    
    def addInstance(self):
        print("Instance unknown, cannot add")
    
    def _retrieveData(self):
        print("instance unknown, no datasource specified")
        self._titles = []
        self._data = []
        self._msg = ""

class FiberList(DataList):
    def __init__(self, parentWidget:tk.Widget, /, title:str, *, dbHandler:DbHandler = None, dynamicSize:bool = False, width:int = 600, height:int = 400, posx:int = 400, posy:int = 150):
        super().__init__(parentWidget, title, dbHandler = dbHandler, dynamicSize=dynamicSize, width=width, height=height, posx=posx, posy=posy)

    def addInstance(self):
        NewFiberForm(self._win, "Add new fiber", dbHandler=self._dbConn)

    def _retrieveData(self):
        success, self._data = self._dbConn.getFibers()
        if not success:
            self._msg = "ERROR: Could not retrieve fiber data from database" 
        self._titles = [key for key in self._data[0]]
        

class LaminaList(DataList):
    def __init__(self, parentWidget:tk.Widget, /, title:str, *, dbHandler:DbHandler = None, dynamicSize:bool = False, width:int = 600, height:int = 400, posx:int = 400, posy:int = 150):
        super().__init__(parentWidget, title, dbHandler = dbHandler, dynamicSize=dynamicSize, width=width, height=height, posx=posx, posy=posy)
    
    def addInstance(self):
        NewLaminaForm(self._win, "Add new lamina", dbHandler=self._dbConn)
    
    def _retrieveData(self):
        success, self._data = self._dbConn.getShortLaminas()
        if not success:
            self._msg = "ERROR: Could not retrieve lamina data from database"
        self._titles = [key for key in self._data[0]]
        

