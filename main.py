import db_sqlite3 as db
from Fiber import *

conn = db.newConnection("fibers.db")

ys80a = Fiber(1, "ys80a", 70000, 70000, 6000, 0.2, 5)

print(f"Name is: {ys80a.name}")