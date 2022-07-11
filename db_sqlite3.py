import sqlite3

def newConnection(filename: str) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(filename)
        # conn.execute("PRAGMA foreign_keys = on")
        return conn
    except:
        print("An error occured...")
        raise

def buildNewDatabase(conn: sqlite3.Connection) -> None:
    try:
        cur = conn.cursor()

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
        print("Fiber database built successfully")
    except:
        print("Error: Could not build database")
        raise

def insertFiber(conn: sqlite3.Connection, fiberdict) -> str:
    try:
        cur = conn.cursor()
        cur.execute("""INSERT INTO fiber(name, type, modulus, strength, density, comment) VALUES (
                        :name,
                        :type,
                        :modulus,
                        :UTS,
                        :rho,
                        :comment
                    )""", fiberdict)
        cur.close()
        return "Fiber added to database"
    except:
        print("Error: Could not add fiber to database") 
        raise

def insertLamina(conn: sqlite3.Connection, laminadict) -> str:
    try:
        cur = conn.cursor()
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
                    )""", laminadict)
        return "Lamina added to database"
    except:
        return "Error: Could not add lamina to database"

def listDbTables(conn: sqlite3.Connection) -> str:
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [
        v[0] for v in cursor.fetchall()
        if v[0] != "sqlite_sequence"
    ]
    cursor.close()
    return tables    
    return None

### TESTING ####

def main() -> None:
    conn = newConnection("fibers.db")
    buildNewDatabase(conn)
    cur = conn.cursor()
    
    print(listDbTables(conn))

    testfibers = getTestFibers(3)
    for fiber in testfibers:
        print(fiber.dictFormat)
        print(insertFiber(conn, fiber.dictFormat))

    for row in cur.execute('SELECT * FROM fibertype'):
        print(row)

    conn.close()

if __name__ == "__main__":
    from Fiber import Fiber, getTestFibers
    main()