from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Get all route
@app.route('/books', methods=['GET'])
def get_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    rows = cursor.fetchall()
    conn.close()

    books = []
    for row in rows:
        book = {
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'genre': row[3],
            'status': row[4]
        }
        books.append(book)
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True)