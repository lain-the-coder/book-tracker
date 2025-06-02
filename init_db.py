import sqlite3

# Connect to database (creates books.db if it doesn't exist)
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT,
        status TEXT CHECK(status IN ('Want to Read', 'Reading', 'Finished')) NOT NULL
    )
''')

conn.commit()
conn.close()

print("Database initialized.")