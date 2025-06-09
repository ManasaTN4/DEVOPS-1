import sqlite3

def add_student(name, email, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    try:
        cursor.execute("INSERT INTO students (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        print(f"Student '{name}' added successfully.")
    except sqlite3.IntegrityError:
        print("Error: Email already exists.")
    conn.close()

if __name__ == "__main__":
    # Change these values to add your student
    add_student("Test Student", "test@example.com", "1234")
    add_student("Manasa TN", "Mansa@gmail.com", "1234")
    add_student("Priyanka", "Priyanka@gmail.com", "1234")
    add_student("Swetha", "Swetha@gmail.com", "1234")
