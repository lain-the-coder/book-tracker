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

# GET by ID route
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()

    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    
    result = {
        'id': book[0],
        'title': book[1],
        'author': book[2],
        'genre': book[3],
        'status': book[4]
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)