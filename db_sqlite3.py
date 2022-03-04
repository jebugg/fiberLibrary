import sqlite3

def newConnection(filename: str) -> sqlite3.Connection:
    return sqlite3.connect(filename)


