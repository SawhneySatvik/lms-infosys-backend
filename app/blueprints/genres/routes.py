from flask import request, jsonify, current_app
from . import genres_bp
from .forms import GenreForm
from ... import db
from ...models.genres import Genre
from ...models.books import Book
from ...models.libraries import Library
from ...utils.role_manager import role_required
from datetime import datetime

@genres_bp.route('', methods=['POST'])
@role_required(['Librarian'])
def create_genre():
    form = GenreForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        librarian = request.current_user
        library = Library.query.filter_by(library_id=librarian.library_id).first()
        if not library:
            return jsonify({"error": "Librarian's library not found"}), 404

        # Check for existing genre
        if Genre.query.filter_by(name=form.name.data).first():
            return jsonify({"error": "Genre name already exists"}), 400

        # Create genre
        new_genre = Genre(
            name=form.name.data,
            description=form.description.data,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(new_genre)
        db.session.commit()

        return jsonify({
            "message": "Genre created successfully",
            "genre_id": str(new_genre.genre_id)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create genre: {str(e)}"}), 500

@genres_bp.route('', methods=['GET'])
@role_required(['Librarian', 'Member'])
def list_genres():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        query = Genre.query

        # Optional filter
        name = request.args.get('name')
        if name:
            query = query.filter(Genre.name.ilike(f'%{name}%'))

        genres = query.paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({
            "genres": [{
                "genre_id": str(genre.genre_id),
                "name": genre.name,
                "description": genre.description,
                "created_at": genre.created_at.isoformat(),
                "updated_at": genre.updated_at.isoformat()
            } for genre in genres.items],
            "total": genres.total,
            "pages": genres.pages,
            "page": page
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to list genres: {str(e)}"}), 500

@genres_bp.route('/<genre_id>', methods=['GET'])
@role_required(['Librarian', 'Member'])
def get_genre(genre_id):
    try:
        genre = Genre.query.filter_by(genre_id=genre_id).first()
        if not genre:
            return jsonify({"error": "Genre not found"}), 404

        return jsonify({
            "genre": {
                "genre_id": str(genre.genre_id),
                "name": genre.name,
                "description": genre.description,
                "created_at": genre.created_at.isoformat(),
                "updated_at": genre.updated_at.isoformat()
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get genre: {str(e)}"}), 500

@genres_bp.route('/<genre_id>', methods=['PATCH'])
@role_required(['Librarian'])
def update_genre(genre_id):
    form = GenreForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        librarian = request.current_user
        library = Library.query.filter_by(library_id=librarian.library_id).first()
        if not library:
            return jsonify({"error": "Librarian's library not found"}), 404

        genre = Genre.query.filter_by(genre_id=genre_id).first()
        if not genre:
            return jsonify({"error": "Genre not found"}), 404

        # Check for duplicate name
        if form.name.data != genre.name and Genre.query.filter_by(name=form.name.data).first():
            return jsonify({"error": "Genre name already exists"}), 400

        # Update genre fields
        if form.name.data:
            genre.name = form.name.data
        if form.description.data is not None:
            genre.description = form.description.data
        genre.updated_at = datetime.now()

        db.session.commit()

        return jsonify({
            "message": "Genre updated successfully",
            "genre_id": str(genre.genre_id)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update genre: {str(e)}"}), 500

@genres_bp.route('/<genre_id>', methods=['DELETE'])
@role_required(['Librarian'])
def delete_genre(genre_id):
    try:
        genre = Genre.query.filter_by(genre_id=genre_id).first()
        if not genre:
            return jsonify({"error": "Genre not found"}), 404

        # Remove genre_id from books
        books = Book.query.filter(Book.genre_ids.contains([genre.genre_id])).all()
        for book in books:
            book.genre_ids = [gid for gid in book.genre_ids if gid != genre.genre_id]
            book.updated_at = datetime.now()
            db.session.add(book)

        db.session.delete(genre)
        db.session.commit()

        return jsonify({"message": "Genre deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete genre: {str(e)}"}), 500