import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("""
INSERT OR IGNORE INTO students (name, email, password)
VALUES (?, ?, ?)
""", ("Test Student", "test@example.com", "1234"))
conn.commit()
conn.close()
