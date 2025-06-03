from flask import Flask, jsonify, request
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

# POST route
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre', '')
    status = data.get('status')
    
    # Title/Author/Status validation
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    if not author:
        return jsonify({'error': 'Author is required'}), 400
    if not status:
        return jsonify({'error': 'Status is required'}), 400

    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO books (title, author, genre, status) VALUES (?, ?, ?, ?)',
        (title, author, genre, status)
    )
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()

    new_book = {
        'id': book_id,
        'title': title,
        'author': author,
        'genre': genre,
        'status': status
    }
    return jsonify(new_book), 201

# PUT route
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre', '')
    status = data.get('status')

    # Title/Author/Status validation
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    if not author:
        return jsonify({'error': 'Author is required'}), 400
    if not status:
        return jsonify({'error': 'Status is required'}), 400
    
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()

    if book is None:
        conn.close()
        return jsonify({'error': 'Book not found'}), 404
    
    cursor.execute('''
    UPDATE books
    SET title = ?, author = ?, genre = ?, status = ?
    WHERE id = ?
    ''', (title, author, genre, status, book_id))

    conn.commit()
    conn.close()

    updated_book = {
        'id': book_id,
        'title': title,
        'author': author,
        'genre': genre,
        'status': status
    }

    return jsonify(updated_book)

if __name__ == '__main__':
    app.run(debug=True)