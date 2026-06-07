import sqlite3
import bcrypt
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "space_missions.db")

print(f"Connecting to database at {db_path}...")
conn = sqlite3.connect(db_path)
cur = conn.cursor()


print("Creating Userlogin table...")
cur.execute("""
CREATE TABLE IF NOT EXISTS "Userlogin" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "user" TEXT UNIQUE,
    "usergroup" TEXT,
    "password" TEXT
)
""")

cur.execute("SELECT COUNT(*) FROM Userlogin")
count = cur.fetchone()[0]

if count == 0:
    print("Inserting default users...")
    

    root_hash = bcrypt.hashpw(b"admin", bcrypt.gensalt()).decode()
    user1_hash = bcrypt.hashpw(b"user1", bcrypt.gensalt()).decode()
    
    cur.execute("""
    INSERT INTO Userlogin (id, user, usergroup, password) VALUES (?, ?, ?, ?)
    """, (2, 'root', 'admin', root_hash))
    
    cur.execute("""
    INSERT INTO Userlogin (id, user, usergroup, password) VALUES (?, ?, ?, ?)
    """, (3, 'user1', 'users', user1_hash))
    
    conn.commit()
    print("Default users inserted successfully:")
    print("  - root / admin")
    print("  - user1 / user1")
else:
    print("Userlogin table already contains data. Skipping default user insertion.")

conn.close()
print("Database initialization complete.")
