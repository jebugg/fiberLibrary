
class DbHandler:
    import sqlite3
    def __init__(self, path:str) -> None:
        self._isReady = False
        try:
            self._conn = self.sqlite3.connect(path)
            self._isReady = True
            print("Database connected successfully!")
        except:
            print("Could not connect to database")
    
    @property
    def state(self):
        return self._isReady
    
    def _writeInsertString(self, d:dict):
        colNames = ""
        colVals = ""
        for key in d:
            colNames += key + ", "
            colVals += ":" + key + ", "
        return colNames[:-2], colVals[:-2]
    
    def _insertToTable(self, table:str, data:dict):
        try:
            cur = self._conn.cursor()
            #TODO: Check that dict keys matches with table column names, raise ValueError if not
            columns, variables = self._writeInsertString(data)
            insertString = f"INSERT INTO {table}({columns}) VALUES ({variables})"
            cur.execute(insertString, data)
            cur.close()
            self._conn.commit()
            return True
        except:
            return False
    
    def _writeSelectString(self, table:str, d:dict):
        raise NotImplementedError

    def _getData(self, selectString:str, columns:dict):
        try:
            cur = self._conn.cursor()
            data = cur.execute(selectString).fetchall()
            dictList = []
            for row in data:
                dictList.append({col:row[i] for i,col in enumerate(columns)})  
            return True, dictList
        except:
            return False, 
    def _getColAsList(self, selectString:str):
        try:
            cur = self._conn.cursor()
            data = cur.execute(selectString).fetchall()
            cur.close()
            return [e[0] for e in data]
        except:
            print("Could not retrieve list")
            return None
    
    def _getRowIdFromName(self, selectstring:str):
        try:
            cur = self._conn.cursor()
            data = cur.execute(selectstring).fetchall()
            return data[0][0]
        except:
            return None
        
    def _getUnfilteredData(self, table:str, columns:dict):
        try:
            columnNames = ", ".join([col for col in columns])
            selectString = f"SELECT {columnNames} FROM {table}"
            return self._getData(selectString, columns)
        except:
            return False, [columns]
    
    def _getFilteredEqualAndData(self, table:str, columns:dict, filters:dict):
        try:
            columnNames = ", ".join([col for col in columns])
            filters = " AND ".join([f"{key} = :{key}" for key in filters])
            selectString = f"SELECT {columnNames} FROM {table} WHERE {filters}"
            return self._getData(selectString,columns)
        except:
            return False, [columns]
    
    def _labelEntries(self, data):
        if "use" in data[0]:
            usecases = self.getUsecases()
            if usecases is None:
                return data
            for i,row in enumerate(data):
                if row["use"] is not None:
                    data[i]["use"] = usecases[row["use"] - 1]
        
        if "material" in data[0]:
            materials = self.getMaterials()
            if materials is None:
                return data
            for i,row in enumerate(data):
                if row["material"] is not None:
                    data[i]["material"] = materials[row["material"] - 1]
        return data

    def addFiber(self, fiberData:dict):
        if self._insertToTable("fibers",fiberData):
            return True, "Fiber added to database"
        else:
            return False, "Error: Fiber could not be added to database"
    
    def addLamina(self, laminaData:dict):
        if self._insertToTable("laminas", laminaData): 
            return True, "Lamina added to database"
        else:
            return False, "Error: Lamina could not be added to database"
    
    def getUsecases(self):
        try:
            selectString = "SELECT name FROM usecases"
            return self._getColAsList(selectString)
        except:
            return None
    
    def getMaterials(self):
        try:
            selectString = "SELECT name FROM materials"
            return self._getColAsList(selectString)
        except:
            return None
    
    def getMaterialId(self, name:str):
        try:
            selectString = f"SELECT rowid FROM materials WHERE name IS '{name}'"
            return self._getRowIdFromName(selectString)
        except:
            return None

    def getShortLaminas(self):
        laminaDict = {"rowid":None, "name":None, "use":None, "faw":None}
        success, data = self._getUnfilteredData("laminas", laminaDict)
        return success, self._labelEntries(data)

    def getFibers(self):
        fiberDict = {"rowid":None, "name":None, "material":None, "modulus":None, "uts":None, "rho":None, "comment":None}
        success, data = self._getUnfilteredData("fibers", fiberDict)
        return success, self._labelEntries(data)