from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Author, Book, Review
from scrape_books import scrape_bp
app.register_blueprint(scrape_bp)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/books')
def get_books():
    books = Book.query.all()
    data = []
    for book in books:
        data.append({
            "id": book.id,
            "title": book.title,
            "publication_year": book.publication_year,
            "author": book.author.name,
            "reviews": [{"rating": r.rating, "comment": r.comment} for r in book.reviews]
        })
    return jsonify(data)

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify({
        "id": book.id,
        "title": book.title,
        "publication_year": book.publication_year,
        "author": book.author.name,
        "reviews": [{"rating": r.rating, "comment": r.comment} for r in book.reviews]
    })

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'publication_year', 'author_id')):
        return jsonify({'error': 'Invalid input'}), 400
    new_book = Book(
        title=data['title'],
        publication_year=data['publication_year'],
        author_id=data['author_id']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added'}), 201

@app.route('/books/<int:id>', methods=['PATCH'])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    data = request.get_json()
    if 'title' in data:
        book.title = data['title']
    if 'publication_year' in data:
        book.publication_year = data['publication_year']
    db.session.commit()
    return jsonify({'message': 'Book updated'})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})
