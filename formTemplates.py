from guiFramework import *

class Row:
    def __init__(self, parentWidget, /, rowNum, *, title, msgStd="", msgError=""):
        self._parent = parentWidget
        self._position = rowNum
        self._msgStd = msgStd
        self._msgError = msgError

        self._labelBox = tk.Label(self._parent, text=title+":")
        self._msgBox = tk.Label(self._parent, text=self._msgStd)

        self.update()

    def newMsg(self, nm):
        self._msgStd = nm
        self._msgBox.config(text = nm)

    def displayError(self):
        self._msgBox.config(text=self._msgError)

    def update(self):
        self._labelBox.grid(column=0, row=self._position, sticky=tk.E)
        self._msgBox.grid(column=1, row=self._position, sticky=tk.W)
    
    def changePos(self, np):
        if np > 0 and np != self._position:
            self._position = np
            self.displayBoxes()
    
    def reset(self):
        self._msgBox.config(text=self._msgStd)
        self.update()
    
class EntryRow(Row):
    def __init__(self, parentWidget, /, rowNum:int, *, title:str, datatype=float, msgStd:str="", msgError:str="", editable:bool=True):
        self._datatype = datatype
        self._state = "normal" if editable else "readonly"

        self._inputBox = tk.Entry(parentWidget, state=self._state)

        super().__init__(parentWidget, rowNum, title=title, msgStd=msgStd, msgError=msgError)
        # self.update()

    def update(self):
        self._labelBox.grid(column=0, row=self._position, sticky=tk.E)
        self._inputBox.config(state=self._state)
        self._inputBox.grid(column=1, row=self._position)
        self._msgBox.grid(column=2, row=self._position, sticky=tk.W)

    def getRawEntry(self):
        return self._inputBox.get()
    
    def getEntry(self):
        userVal = self._inputBox.get()
        if "," in userVal and not "." in userVal:
            userVal = ".".join(userVal.split(",")) 
        try:
            if userVal == "" and (self._datatype == int or self._datatype == float):
                return 0
            if self._datatype != str:
                userVal = self._datatype(userVal)
            return userVal
        except:
            self._msgError = "Please make sure data is of type {}".format(self._datatype.__name__)
            self.displayError()
            return TypeError


    def reset(self):
        self._msgBox.config(text=self._msgStd)
        self._inputBox.delete(0, 'end')
        self.update()

    def lock(self):
        self._state = "readonly"
        self.update()
    
    def unlock(self):
        self._state = "normal"
        self.update()

class DropdownRow(Row):
    def __init__(self, parentWidget, /, rowNum:int, *, title:str, msgStd:str="", msgError:str="", editable:bool=True, options:list=None, defaultOption:str="Select..."):
        self._state = "normal" if editable else "readonly"
        self._options = options if options != None else ["-"]
        self._default = defaultOption
        
        self._selected = tk.StringVar()
        self._selected.set(self._default)
        self._dropdown = tk.OptionMenu(parentWidget, self._selected,*options)

        super().__init__(parentWidget, rowNum, title=title, msgStd=msgStd, msgError=msgError)

    def getEntry(self):
        return self._selected.get()

    def update(self):
        self._labelBox.grid(column=0, row=self._position, sticky=tk.E)
        self._dropdown.grid(column=1, row=self._position, sticky=tk.EW)
        self._msgBox.grid(column=2, row=self._position, sticky=tk.W)
    
    def reset(self):
        self._msgBox.config(text=self._msgStd)
        self._selected.set(self._default)
        self.update()


class FiberForm(SubWindow):
    def __init__(self, parentWidget:tk.Widget, /, title:str, *, dbHandler:DbHandler = None, dynamicSize:bool = True, width:int = 600, height:int = 400, posx:int = 400, posy:int = 150):
        super().__init__(parentWidget, title, dbHandler=dbHandler, dynamicSize=dynamicSize, width=width, height=height, posx=posx, posy=posy)
        self._rowNumBtns = 2
        self._header = tk.Label(self._win, text="This is Form v2.0")

        self._form = tk.Frame(self._win)
        self._fields = {}
        self._fields["name"] = EntryRow(self._form, 0, title="Name", datatype=str)
        self._fields["material"] = DropdownRow(self._form, 1, title="Material", options=self._dbConn.getMaterials()) #TODO: Make options materials from db
        self._fields["modulus"] = EntryRow(self._form, 2, title="Youngs Modulus", msgStd="GPa")
        self._fields["uts"] = EntryRow(self._form, 3, title="Strength", msgStd="GPa")
        self._fields["rho"] = EntryRow(self._form, 4, title="Rho", msgStd="kg/m3")
        self._fields["comment"] = EntryRow(self._form, 5, title="Comment", datatype=str)

        self._btn_cancel = tk.Button(self._win, text="Cancel", command=self.close)
        
        self._header.grid(column=0, columnspan=3, row=0)
        self._form.grid(column=0, columnspan=3, row=1)
        self._btn_cancel.grid(column=2, row=self._rowNumBtns, sticky=tk.E, padx=10, pady=10)

    def clearFields(self):
        for key, field in self._fields.items():
            field.reset()
        return None

class NewFiberForm(FiberForm):
    def __init__(self, parentWidget:tk.Widget, /, title:str, *, dbHandler:DbHandler = None, dynamicSize:bool = True, width:int = 600, height:int = 400, posx:int = 400, posy:int = 150):
        super().__init__(parentWidget, title, dbHandler=dbHandler, dynamicSize=dynamicSize, width=width, height=height, posx=posx, posy=posy)

        self._btn_add = tk.Button(self._win, text = "Add Fiber", command=self.addData)
        self._btn_clear = tk.Button(self._win, text = "Clear Fields", command=self.clearData)
        
        self._btn_add.grid(column=0, row=self._rowNumBtns)
        self._btn_clear.grid(column=1, row=self._rowNumBtns)

    def addData(self):
        if self._dbConn is not None:
            try:
                fiberData = {}
                for key, field in self._fields.items():
                    if key == "material":
                        fiberData[key] = self._dbConn.getMaterialId(field.getEntry())
                    else:
                        fiberData[key] = field.getEntry()

                success, message = self._dbConn.addFiber(fiberData)
                if not success:
                    print(message)
                    raise
                self.close()
            except:
                print("Failed to add data to library. Please check inputs")
        else:
            print("Database not connected!")

    def clearData(self):
        for key, field in self._fields.items():
            field.reset()

class AlterFiberForm(FiberForm):
    def __init__(self, parentWidget, /, title, *, dynamicSize:bool = True, width:int = 600, height:int = 400, posx:int = 400, posy:int = 150):
        super().__init__(parentWidget, title, dynamicSize=dynamicSize, width=width, height=height, posx=posx, posy=posy)

        self._btn_update = tk.Button(self._win, text = "Update Fiber", command=self.updateData)
        self._btn_reset = tk.Button(self._win, text = "Reset form", command=self.retrieveData)

        self._btn_update.grid(column=0, row=self._rowNumBtns)
        self._btn_reset.grid(column=0, row=self._rowNumBtns)

    def updateData(self):
        print("this button should push an update of all data in the form to the database")
        print("...but currently it does nothing")

    def retrieveData(self):
        print("This function will retrieve fiber data from server")

class LaminaForm(SubWindow):
    def __init__(self, parentWidget:tk.Widget, /, title:str, *, dbHandler = None, dynamicSize:bool = True, width:int = 600, height:int = 400, posx:int = 400, posy:int = 150):
        super().__init__(parentWidget, title, dbHandler=dbHandler, dynamicSize=dynamicSize, width=width, height=height, posx=posx, posy=posy)
        self._rowNumBtns = 2
        self._header = tk.Label(self._win, text="This is Lamina form v0.1")

        self._form = tk.Frame(self._win)

        self._fields = {}
        self._fields["name"] = EntryRow(self._form, 1, title="Name", datatype=str, msgError="Invalid name")
        self._fields["fiber"] = DropdownRow(self._form, 2, title="Fiber", options=[1,2,3])
        self._fields["matrix"] = DropdownRow(self._form, 3, title="Matrix", options=[1,2,3])
        self._fields["weave"] = DropdownRow(self._form, 4, title="Weave", options=[1,2,3])
        self._fields["use"] = DropdownRow(self._form, 5, title="Usecase", options=[1,2,3])
        self._fields["E1"] = EntryRow(self._form, 6, title="E1", msgStd="GPa")
        self._fields["E2"] = EntryRow(self._form, 7, title="E2", msgStd="GPa")
        self._fields["G12"] = EntryRow(self._form, 8, title="G12", msgStd="GPa")
        self._fields["nu"] = EntryRow(self._form, 9, title="Shear factor")
        self._fields["vff"] = EntryRow(self._form, 10, title="Vff")
        self._fields["faw"] = EntryRow(self._form, 11, title="FAW", msgStd="g/m2")
        self._fields["thickness"] = EntryRow(self._form, 12, title="Thickness", msgStd="mm")
        self._fields["comment"] = EntryRow(self._form, 13, title="Comment", datatype=str)

        self._btn_cancel = tk.Button(self._win, text="Cancel", command=self.close)
        
        self._header.grid(column=0, columnspan=3, row=0)
        self._form.grid(column=0, columnspan=3, row=1)
        self._btn_cancel.grid(column=2, row=self._rowNumBtns, sticky=tk.E, padx=10, pady=10)

    def clearFields(self):
        for key, field in self._fields.items():
            field.reset()
        return None

class NewLaminaForm(LaminaForm):
    def __init__(self, parentWidget:tk.Widget, /, title:str, *, dbHandler = None, dynamicSize:bool = True, width:int = 600, height:int = 400, posx:int = 400, posy:int = 150):
        super().__init__(parentWidget, title, dbHandler=dbHandler, dynamicSize=dynamicSize, width=width, height=height, posx=posx, posy=posy)

        self._btn_add = tk.Button(self._win, text = "Add Fiber", command=self.addData)
        self._btn_clear = tk.Button(self._win, text = "Clear Fields", command=self.clearData)
        
        self._btn_add.grid(column=0, row=self._rowNumBtns)
        self._btn_clear.grid(column=1, row=self._rowNumBtns)
    
    def addData(self):
        if self._dbConn is not None:
            try:
                laminaData = {}
                for key, field in self._fields.items():
                    laminaData[key] = field.getEntry()

                success, msg = self._dbConn.addLamina(laminaData)
                if not success:
                    raise
                self.close()
            except:
                print("Failed to add data to library. Please check inputs")
        else:
            print("Database not connected!")

    def clearData(self):
        for key, field in self._fields.items():
            field.reset()

class AlterLaminaForm(LaminaForm):
    def __init__(self, parentWidget:tk.Widget, /, title:str, *, dynamicSize:bool = True, width:int = 600, height:int = 400, posx:int = 400, posy:int = 150):
        super().__init__(parentWidget, title, dynamicSize=dynamicSize, width=width, height=height, posx=posx, posy=posy)

        self._btn_update = tk.Button(self._win, text = "Update Lamina", command=self.updateData)
        self._btn_reset = tk.Button(self._win, text = "Reset form", command=self.retrieveData)
        self._btn_update.grid()

    def updateData(self):
        print("this button should push an update of all data in the form to the database")
        print("...but currently it does nothing")
    
    def retrieveData(self):
        print("This function will retrieve lamina data from server")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Root window")
    msg = tk.Label(root, text="this is the root window                ").grid(column=0,row=0)
    form = NewFiberForm(root, "Testform")

    root.mainloop()