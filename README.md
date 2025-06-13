# Book Review Platform

A Flask-based RESTful API that manages books, authors, and reviews. Features include web scraping from Project Gutenberg and comprehensive CRUD operations.

## Features

- RESTful API endpoints for books, authors, and reviews
- Book data scraping from Project Gutenberg
- SQLAlchemy ORM with relationship management
- Database migrations using Flask-Migrate
- Error handling and input validation
- Automatic database seeding

## Technology Stack

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- BeautifulSoup4
- SQLite

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd book-review-platform
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Initialize and apply database migrations:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. Seed the database:
    ```bash
    python seed.py
    ```

## API Endpoints

### Books
- `GET /books` - List all books
- `GET /books/<id>` - Get a specific book
- `POST /books` - Create a new book
- `PATCH /books/<id>` - Update a book
- `DELETE /books/<id>` - Delete a book

### Authors
- `GET /authors` - List all authors

### Web Scraping
- `GET /scrape` - Scrape books from Project Gutenberg

## Request/Response Examples

### Create a Book
```json
POST /books
{
    "title": "New Book",
    "publication_year": 2023,
    "author_id": 1
}
```

### Get Book Response
```json
{
    "id": 1,
    "title": "1984",
    "publication_year": 1949,
    "author": "George Orwell",
    "reviews": [
        {
            "id": 1,
            "rating": 5,
            "comment": "Amazing book!"
        }
    ]
}
```

## Development

1. Start the development server:
    ```bash
    flask run
    ```

2. Access the API at `http://localhost:5000`

## Database Schema

- Authors
  - id (Primary Key)
  - name

- Books
  - id (Primary Key)
  - title
  - publication_year
  - author_id (Foreign Key)
  - created_at

- Reviews
  - id (Primary Key)
  - rating
  - comment
  - created_at

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 500: Server Error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License