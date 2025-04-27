from flask import request, jsonify, current_app
from . import authors_bp
from .forms import AuthorForm
from ... import db
from ...models.authors import Author
from ...models.libraries import Library
from ...utils.role_manager import role_required
from ...config import Config
from supabase import create_client, Client
from datetime import datetime

# Initialize Supabase client
supabase: Client = create_client(Config.SUPABASE_PROJECT_URL, Config.SUPABASE_ANON_PUBLIC_KEY)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@authors_bp.route('', methods=['POST'])
@role_required(['Librarian'])
def create_author():
    form = AuthorForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        librarian = request.current_user
        library = Library.query.filter_by(library_id=librarian.library_id).first()
        if not library:
            return jsonify({"error": "Librarian's library not found"}), 404

        # Upload author_image if provided
        author_image_url = None
        if 'author_image' in request.files:
            file = request.files['author_image']
            if file and allowed_file(file.filename):
                filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
                supabase.storage.from_('author_images').upload(
                    path=filename,
                    file=file.stream,
                    file_options={"content-type": file.content_type}
                )
                author_image_url = supabase.storage.from_('author_images').get_public_url(filename)

        # Create author
        new_author = Author(
            name=form.name.data,
            bio=form.bio.data,
            author_image=author_image_url,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_author)
        db.session.commit()

        return jsonify({
            "message": "Author created successfully",
            "author_id": str(new_author.author_id)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create author: {str(e)}"}), 500

@authors_bp.route('', methods=['GET'])
@role_required(['Librarian', 'Member'])
def list_authors():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        query = Author.query

        # Optional filter
        name = request.args.get('name')
        if name:
            query = query.filter(Author.name.ilike(f'%{name}%'))

        authors = query.paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({
            "authors": [{
                "author_id": str(author.author_id),
                "name": author.name,
                "bio": author.bio,
                "author_image": author.author_image,
                "book_ids": [str(bid) for bid in author.book_ids or []],
                "created_at": author.created_at.isoformat(),
                "updated_at": author.updated_at.isoformat()
            } for author in authors.items],
            "total": authors.total,
            "pages": authors.pages,
            "page": page
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to list authors: {str(e)}"}), 500

@authors_bp.route('/<author_id>', methods=['GET'])
@role_required(['Librarian', 'Member'])
def get_author(author_id):
    try:
        author = Author.query.filter_by(author_id=author_id).first()
        if not author:
            return jsonify({"error": "Author not found"}), 404

        return jsonify({
            "author": {
                "author_id": str(author.author_id),
                "name": author.name,
                "bio": author.bio,
                "author_image": author.author_image,
                "book_ids": [str(bid) for bid in author.book_ids or []],
                "created_at": author.created_at.isoformat(),
                "updated_at": author.updated_at.isoformat()
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get author: {str(e)}"}), 500

@authors_bp.route('/<author_id>', methods=['PATCH'])
@role_required(['Librarian'])
def update_author(author_id):
    form = AuthorForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        librarian = request.current_user
        library = Library.query.filter_by(library_id=librarian.library_id).first()
        if not library:
            return jsonify({"error": "Librarian's library not found"}), 404

        author = Author.query.filter_by(author_id=author_id).first()
        if not author:
            return jsonify({"error": "Author not found"}), 404

        # Upload new author_image if provided
        author_image_url = author.author_image
        if 'author_image' in request.files:
            file = request.files['author_image']
            if file and allowed_file(file.filename):
                filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
                supabase.storage.from_('author_images').upload(
                    path=filename,
                    file=file.stream,
                    file_options={"content-type": file.content_type}
                )
                author_image_url = supabase.storage.from_('author_images').get_public_url(filename)

        # Update author fields
        if form.name.data:
            author.name = form.name.data
        if form.bio.data is not None:
            author.bio = form.bio.data
        author.author_image = author_image_url
        author.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            "message": "Author updated successfully",
            "author_id": str(author.author_id)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update author: {str(e)}"}), 500

@authors_bp.route('/<author_id>', methods=['DELETE'])
@role_required(['Librarian'])
def delete_author(author_id):
    try:
        author = Author.query.filter_by(author_id=author_id).first()
        if not author:
            return jsonify({"error": "Author not found"}), 404

        # Remove author_id from books
        books = Book.query.filter(Book.author_ids.contains([author.author_id])).all()
        for book in books:
            book.author_ids = [aid for aid in book.author_ids if aid != author.author_id]
            book.updated_at = datetime.utcnow()
            db.session.add(book)

        db.session.delete(author)
        db.session.commit()

        return jsonify({"message": "Author deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete author: {str(e)}"}), 500