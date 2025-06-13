from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from models import db, Author, Book, Review
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Register scraping blueprint
from scrape_books import scrape_bp
app.register_blueprint(scrape_bp)

# Simple index route to confirm it's working
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Book Review Platform API"})

# OPTIONAL: basic routes if you want to test them
@app.route('/authors')
def get_authors():
    authors = Author.query.all()
    return jsonify([{"id": a.id, "name": a.name} for a in authors])

@app.route('/books')
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@app.route('/books/<int:book_id>')
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    if not all(k in data for k in ('title', 'publication_year', 'author_id')):
        abort(400, description="Missing required fields")
    
    try:
        book = Book(
            title=data['title'],
            publication_year=data['publication_year'],
            author_id=data['author_id']
        )
        db.session.add(book)
        db.session.commit()
        return jsonify(book.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Invalid author ID")

@app.route('/books/<int:book_id>', methods=['PATCH'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    
    if 'title' in data:
        book.title = data['title']
    if 'publication_year' in data:
        book.publication_year = data['publication_year']
    
    db.session.commit()
    return jsonify(book.to_dict())

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': str(error.description)}), 400

if __name__ == '__main__':
    app.run(debug=True)
