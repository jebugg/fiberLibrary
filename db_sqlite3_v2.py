import sqlite3

class DbHandler:
    def __init__(self, path):
        self._isReady = False
        try:
            self._conn = sqlite3.connect(path)
            self._isReady = True
        except:
            print("An error occured... Could not connect to the specified database")
            raise
    
    def addFiber(self, fiberData):
        try:
            cur = self._conn.cursor()
            cur.execute("""INSERT INTO fiber(name, type, modulus, strength, density, comment) VALUES (
                        :name,
                        :type,
                        :modulus,
                        :UTS,
                        :rho,
                        :comment
                    )""", fiberData)
            cur.close()
            return True, "Fiber added to database"
        except:
            return False, "Error: Could not add fiber to database"

    def insertLamina(self, laminaData):
        try:
            cur = self._conn.cursor()
            cur.execute("""INSERT INTO lamina(name, fiber, use, e1, e2, g12, nu, rho, faw, thickness, comment) VALUES (
                        :name,
                        :fiber,
                        :use,
                        :e1,
                        :e2,
                        :g12,
                        :nu,
                        :rho,
                        :faw, 
                        :thickness,
                        :comment
                    )""", laminaData)
            return True, "Lamina added to database"
        except:
            return False, "Error: Could not add lamina to database"
    
def listDbTables(dbh: DbHandler) -> str:
    cursor = dbh._conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [
        v[0] for v in cursor.fetchall()
        if v[0] != "sqlite_sequence"
    ]
    cursor.close()
    return tables    

def buildNewDatabase(dbh: DbHandler) -> None:
    try:
        cur = dbh._conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS fibertype (
                        id INTEGER PRIMARY KEY ASC,
                        name TEXT
                    )
                """)
        fibertypes = ["Aramid", "Carbon", "Glass"]
        for fibertype in fibertypes:
            cur.execute("""INSERT INTO fibertype(name) VALUES (?)""",(fibertype,))
        
        cur.execute("""CREATE TABLE IF NOT EXISTS usecase (
                        id INTEGER PRIMARY KEY ASC,
                        name TEXT
                    )
                """)
        usecases = ["High Stiffness", "Stiffness", "Geometry", "Strength", "High Strength"]
        for usecase in usecases:
            cur.execute("""INSERT INTO usecase(name) VALUES (?)""", (usecase,))

        cur.execute("""CREATE TABLE IF NOT EXISTS fiber (
                        id INTEGER PRIMARY KEY ASC, 
                        name TEXT, 
                        modulus REAL, 
                        strength REAL, 
                        density REAL, 
                        type INTEGER,
                        comment TEXT,
                        FOREIGN KEY(type) REFERENCES fibertype(id))
                 """)

        cur.execute("""CREATE TABLE IF NOT EXISTS lamina (
                        id INTEGER PRIMARY KEY ASC,
                        name TEXT, 
                        fiber INTEGER,
                        use INTEGER,
                        e1 REAL,
                        e2 REAL,
                        g12 REAL,
                        nu REAL,
                        rho REAL,
                        faw TEXT,
                        thickness REAL,
                        comment TEXT,
                        FOREIGN KEY(fiber) REFERENCES fiber(id),
                        FOREIGN KEY(use) REFERENCES usecase(id)
                    )
                """)
        cur.close()
        print("Fiber database built successfully")
    except:
        print("Error: Could not build database")
        raise