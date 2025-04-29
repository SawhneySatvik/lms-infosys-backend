from flask import request, jsonify
from . import admin_bp
from .forms import SettingsForm
from ... import db
from ...models.books import Book
from ...models.users import User
from ...models.borrow_transactions import BorrowTransaction
from ...models.fines import Fine
from ...models.libraries import Library
from ...utils.role_manager import role_required
from sqlalchemy import func
from datetime import datetime

@admin_bp.route('/dashboard', methods=['GET'])
@role_required(['Admin'])
def dashboard():
    try:
        admin = request.current_user
        library_id = admin.library_id

        total_books = Book.query.filter_by(library_id=library_id).count()
        total_members = User.query.filter_by(library_id=library_id, role='Member').count()
        total_librarians = User.query.filter_by(library_id=library_id, role='Librarian').count()
        active_borrowings = BorrowTransaction.query.filter_by(library_id=library_id, returned=False).count()
        outstanding_fines = db.session.query(func.sum(Fine.amount)).filter(Fine.library_id == library_id, Fine.paid == False).scalar() or 0

        return jsonify({
            "total_books": total_books,
            "total_members": total_members,
            "total_librarians": total_librarians,
            "active_borrowings": active_borrowings,
            "outstanding_fines": float(outstanding_fines)
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to load dashboard: {str(e)}"}), 500

@admin_bp.route('/settings', methods=['GET'])
@role_required(['Admin'])
def get_settings():
    try:
        admin = request.current_user
        library = Library.query.filter_by(library_id=admin.library_id).first()
        if not library:
            return jsonify({"error": "Library not found"}), 404

        return jsonify({
            "fine_rate": float(library.fine_rate) if library.fine_rate is not None else None,
            "max_borrow_days": library.max_borrow_days
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to get settings: {str(e)}"}), 500

@admin_bp.route('/settings', methods=['PATCH'])
@role_required(['Admin'])
def update_settings():
    form = SettingsForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        admin = request.current_user
        library = Library.query.filter_by(library_id=admin.library_id).first()
        if not library:
            return jsonify({"error": "Library not found"}), 404

        if form.fine_rate.data is not None:
            library.fine_rate = form.fine_rate.data
        if form.max_borrow_days.data is not None:
            library.max_borrow_days = form.max_borrow_days.data
        library.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify({"message": "Settings updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update settings: {str(e)}"}), 500