from flask import Blueprint, jsonify, current_app
import requests
from bs4 import BeautifulSoup
from models import db, Book, Author

scrape_bp = Blueprint('scrape_bp', __name__)

def scrape():
    try:
        url = 'https://www.gutenberg.org/ebooks/bookshelf/37'
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        books_added = 0
        authors_added = 0

        with current_app.app_context():
            for item in soup.select('.booklink')[:5]:
                try:
                    title = item.select_one('.title').get_text(strip=True)
                    author_name = item.select_one('.subtitle').get_text(strip=True)

                    # Skip if either title or author is empty
                    if not title or not author_name:
                        continue

                    author = Author.query.filter_by(name=author_name).first()
                    if not author:
                        author = Author(name=author_name)
                        db.session.add(author)
                        authors_added += 1

                    book_exists = Book.query.filter_by(title=title, author_id=author.id).first()
                    if not book_exists:
                        book = Book(title=title, publication_year=1900, author=author)
                        db.session.add(book)
                        books_added += 1

                except Exception as e:
                    current_app.logger.error(f"Error processing book: {str(e)}")
                    continue

            db.session.commit()

        return {'status': 'success', 'books_added': books_added, 'authors_added': authors_added}

    except requests.RequestException as e:
        return {'status': 'error', 'message': f"Failed to fetch data: {str(e)}"}
    except Exception as e:
        return {'status': 'error', 'message': f"An error occurred: {str(e)}"}

@scrape_bp.route('/scrape')
def scrape_route():
    result = scrape()
    return jsonify(result)
