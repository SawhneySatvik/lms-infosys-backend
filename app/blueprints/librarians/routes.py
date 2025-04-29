from flask import request, jsonify
from . import librarians_bp
from .forms import LibrarianUpdateForm
from ... import db
from ...models.users import User
from ...utils.role_manager import role_required
from datetime import datetime

@librarians_bp.route('', methods=['GET'])
@role_required(['Admin'])
def list_librarians():
    try:
        admin = request.current_user
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        librarians = User.query.filter_by(library_id=admin.library_id, role='Librarian').paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({
            "librarians": [{
                "user_id": str(librarian.user_id),
                "name": librarian.name,
                "email": librarian.email,
                "is_active": librarian.is_active
            } for librarian in librarians.items],
            "total": librarians.total,
            "pages": librarians.pages,
            "page": page
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to list librarians: {str(e)}"}), 500

@librarians_bp.route('/<librarian_id>', methods=['GET'])
@role_required(['Admin'])
def get_librarian(librarian_id):
    try:
        admin = request.current_user
        librarian = User.query.filter_by(user_id=librarian_id, library_id=admin.library_id, role='Librarian').first()
        if not librarian:
            return jsonify({"error": "Librarian not found"}), 404
        return jsonify({
            "user_id": str(librarian.user_id),
            "name": librarian.name,
            "email": librarian.email,
            "is_active": librarian.is_active
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to get librarian: {str(e)}"}), 500

@librarians_bp.route('/<librarian_id>', methods=['PATCH'])
@role_required(['Admin'])
def update_librarian(librarian_id):
    form = LibrarianUpdateForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        admin = request.current_user
        librarian = User.query.filter_by(user_id=librarian_id, library_id=admin.library_id, role='Librarian').first()
        if not librarian:
            return jsonify({"error": "Librarian not found"}), 404

        if form.name.data:
            librarian.name = form.name.data
        if form.email.data:
            librarian.email = form.email.data
        if form.is_active.data is not None:
            librarian.is_active = form.is_active.data
        librarian.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify({"message": "Librarian updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update librarian: {str(e)}"}), 500

@librarians_bp.route('/<librarian_id>', methods=['DELETE'])
@role_required(['Admin'])
def delete_librarian(librarian_id):
    try:
        admin = request.current_user
        librarian = User.query.filter_by(user_id=librarian_id, library_id=admin.library_id, role='Librarian').first()
        if not librarian:
            return jsonify({"error": "Librarian not found"}), 404

        db.session.delete(librarian)
        db.session.commit()
        return jsonify({"message": "Librarian deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete librarian: {str(e)}"}), 500