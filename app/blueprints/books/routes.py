from flask import request, jsonify, current_app
from . import books_bp
from .forms import BookForm, BookUpdateForm
from ... import db
from ...models.books import Book
from ...models.authors import Author
from ...models.genres import Genre
from ...models.libraries import Library
from ...utils.role_manager import role_required
from ...config import Config
from supabase import create_client, Client
from datetime import datetime
from uuid import UUID
import re

# Initialize Supabase client
supabase: Client = create_client(Config.SUPABASE_PROJECT_URL, Config.SUPABASE_ANON_PUBLIC_KEY)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@books_bp.route('', methods=['POST'])
@role_required(['Librarian'])
def create_book():
    form = BookForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        librarian = request.current_user
        library = Library.query.filter_by(library_id=librarian.library_id).first()
        if not library:
            return jsonify({"error": "Librarian's library not found"}), 404

        # Validate author_ids and genre_ids
        author_ids = form.author_ids.data or []
        genre_ids = form.genre_ids.data or []
        if author_ids and not all(Author.query.filter_by(author_id=aid).first() for aid in author_ids):
            return jsonify({"error": "Invalid author_id"}), 400
        if genre_ids and not all(Genre.query.filter_by(genre_id=gid).first() for gid in genre_ids):
            return jsonify({"error": "Invalid genre_id"}), 400

        # Upload book_image if provided
        book_image_url = None
        if 'book_image' in request.files:
            file = request.files['book_image']
            if file and allowed_file(file.filename):
                filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
                supabase.storage.from_('book_images').upload(
                    path=filename,
                    file=file.stream,
                    file_options={"content-type": file.content_type}
                )
                book_image_url = supabase.storage.from_('book_images').get_public_url(filename)

        # Parse published_date
        published_date = None
        if form.published_date.data:
            published_date = datetime.strptime(form.published_date.data, '%Y-%m-%d')

        # Create book
        new_book = Book(
            library_id=librarian.library_id,
            title=form.title.data,
            isbn=form.isbn.data,
            description=form.description.data,
            publisher_name=form.publisher_name.data,
            total_copies=form.total_copies.data,
            available_copies=form.total_copies.data,
            reserved_copies=0,
            book_image=book_image_url,
            author_ids=author_ids,
            genre_ids=genre_ids,
            published_date=published_date,
            added_on=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_book)
        db.session.flush()

        # Update authors' book_ids
        for author_id in author_ids:
            author = Author.query.filter_by(author_id=author_id).first()
            if author:
                author.book_ids = list(set(author.book_ids or []) | {new_book.book_id})
                author.updated_at = datetime.utcnow()
                db.session.add(author)

        db.session.commit()

        return jsonify({
            "message": "Book created successfully",
            "book_id": str(new_book.book_id)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create book: {str(e)}"}), 500

@books_bp.route('', methods=['GET'])
@role_required(['Librarian', 'Member'])
def list_books():
    try:
        user = request.current_user
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        query = Book.query.filter_by(library_id=user.library_id)

        # Optional filters
        title = request.args.get('title')
        author_id = request.args.get('author_id')
        genre_id = request.args.get('genre_id')
        if title:
            query = query.filter(Book.title.ilike(f'%{title}%'))
        if author_id:
            query = query.filter(Book.author_ids.contains([UUID(author_id)]))
        if genre_id:
            query = query.filter(Book.genre_ids.contains([UUID(genre_id)]))

        books = query.paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({
            "books": [{
                "book_id": str(book.book_id),
                "title": book.title,
                "isbn": book.isbn,
                "description": book.description,
                "publisher_name": book.publisher_name,
                "total_copies": book.total_copies,
                "available_copies": book.available_copies,
                "reserved_copies": book.reserved_copies,
                "book_image": book.book_image,
                "author_ids": [str(aid) for aid in book.author_ids or []],
                "genre_ids": [str(gid) for gid in book.genre_ids or []],
                "published_date": book.published_date.isoformat() if book.published_date else None,
                "added_on": book.added_on.isoformat(),
                "updated_at": book.updated_at.isoformat()
            } for book in books.items],
            "total": books.total,
            "pages": books.pages,
            "page": page
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to list books: {str(e)}"}), 500

@books_bp.route('/<book_id>', methods=['GET'])
@role_required(['Librarian', 'Member'])
def get_book(book_id):
    try:
        user = request.current_user
        book = Book.query.filter_by(book_id=book_id, library_id=user.library_id).first()
        if not book:
            return jsonify({"error": "Book not found"}), 404

        return jsonify({
            "book": {
                "book_id": str(book.book_id),
                "title": book.title,
                "isbn": book.isbn,
                "description": book.description,
                "publisher_name": book.publisher_name,
                "total_copies": book.total_copies,
                "available_copies": book.available_copies,
                "reserved_copies": book.reserved_copies,
                "book_image": book.book_image,
                "author_ids": [str(aid) for aid in book.author_ids or []],
                "genre_ids": [str(gid) for gid in book.genre_ids or []],
                "published_date": book.published_date.isoformat() if book.published_date else None,
                "added_on": book.added_on.isoformat(),
                "updated_at": book.updated_at.isoformat()
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get book: {str(e)}"}), 500

@books_bp.route('/<book_id>', methods=['PATCH'])
@role_required(['Librarian'])
def update_book(book_id):
    form = BookUpdateForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        librarian = request.current_user
        book = Book.query.filter_by(book_id=book_id, library_id=librarian.library_id).first()
        if not book:
            return jsonify({"error": "Book not found"}), 404

        # Validate author_ids and genre_ids
        author_ids = form.author_ids.data or book.author_ids
        genre_ids = form.genre_ids.data or book.genre_ids
        if author_ids and not all(Author.query.filter_by(author_id=aid).first() for aid in author_ids):
            return jsonify({"error": "Invalid author_id"}), 400
        if genre_ids and not all(Genre.query.filter_by(genre_id=gid).first() for gid in genre_ids):
            return jsonify({"error": "Invalid genre_id"}), 400

        # Upload new book_image if provided
        book_image_url = book.book_image
        if 'book_image' in request.files:
            file = request.files['book_image']
            if file and allowed_file(file.filename):
                filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
                supabase.storage.from_('book_images').upload(
                    path=filename,
                    file=file.stream,
                    file_options={"content-type": file.content_type}
                )
                book_image_url = supabase.storage.from_('book_images').get_public_url(filename)

        # Update book fields
        if form.title.data:
            book.title = form.title.data
        if form.isbn.data:
            book.isbn = form.isbn.data
        if form.description.data is not None:
            book.description = form.description.data
        if form.publisher_name.data is not None:
            book.publisher_name = form.publisher_name.data
        if form.total_copies.data:
            delta = form.total_copies.data - book.total_copies
            book.total_copies = form.total_copies.data
            book.available_copies += delta
        book.book_image = book_image_url
        book.author_ids = author_ids
        book.genre_ids = genre_ids
        if form.published_date.data:
            book.published_date = datetime.strptime(form.published_date.data, '%Y-%m-%d')
        book.updated_at = datetime.utcnow()

        # Update authors' book_ids
        old_author_ids = set(book.author_ids or [])
        new_author_ids = set(author_ids)
        for author_id in old_author_ids - new_author_ids:
            author = Author.query.filter_by(author_id=author_id).first()
            if author:
                author.book_ids = list(set(author.book_ids or []) - {book.book_id})
                author.updated_at = datetime.utcnow()
                db.session.add(author)
        for author_id in new_author_ids - old_author_ids:
            author = Author.query.filter_by(author_id=author_id).first()
            if author:
                author.book_ids = list(set(author.book_ids or []) | {book.book_id})
                author.updated_at = datetime.utcnow()
                db.session.add(author)

        db.session.commit()

        return jsonify({
            "message": "Book updated successfully",
            "book_id": str(book.book_id)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update book: {str(e)}"}), 500

@books_bp.route('/<book_id>', methods=['DELETE'])
@role_required(['Librarian'])
def delete_book(book_id):
    try:
        librarian = request.current_user
        book = Book.query.filter_by(book_id=book_id, library_id=librarian.library_id).first()
        if not book:
            return jsonify({"error": "Book not found"}), 404

        # Update authors' book_ids
        for author_id in book.author_ids or []:
            author = Author.query.filter_by(author_id=author_id).first()
            if author:
                author.book_ids = list(set(author.book_ids or []) - {book.book_id})
                author.updated_at = datetime.utcnow()
                db.session.add(author)

        db.session.delete(book)
        db.session.commit()

        return jsonify({"message": "Book deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete book: {str(e)}"}), 500