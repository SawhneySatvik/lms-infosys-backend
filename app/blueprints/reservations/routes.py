from flask import request, jsonify
from . import reservation_bp
from datetime import datetime, timedelta
from .forms import ReservationForm, ReservationUpdateForm
from ... import db
from ...models.users import User
from ...models.books import Book
from ...models.reservations import Reservation
from ...models.policies import Policy
from ...utils.role_manager import role_required

@reservation_bp.route('', methods=['POST'])
@role_required(['Member'])
def create_reservation():
    form = ReservationForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400
    member = request.current_user
    book = Book.query.filter_by(book_id=form.book_id.data, library_id=member.library_id).first()
    if not book or book.available_copies <= 0:
        return jsonify({"error": "Book not available"}), 400
    policy = Policy.query.filter_by(library_id=member.library_id).first()
    if not policy:
        return jsonify({"error": "Library policy not found"}), 404
    existing_reservation = Reservation.query.filter_by(user_id=member.user_id, book_id=book.book_id, status='pending').first()
    if existing_reservation:
        return jsonify({"error": "You already have a pending reservation for this book"}), 400
    reservation = Reservation(
        user_id=member.user_id,
        book_id=book.book_id,
        reserved_at=datetime.now(),
        expires_at=datetime.now() + timedelta(hours=policy.reservation_expiry_hours or 24),
        status='pending'
    )
    book.reserved_copies += 1
    member.reserved_book_ids.append(book.book_id)
    db.session.add(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation created", "reservation_id": str(reservation.reservation_id)}), 201

@reservation_bp.route('', methods=['GET'])
@role_required(['Librarian', 'Member'])
def list_reservations():
    user = request.current_user
    if user.role == 'Librarian':
        reservations = Reservation.query.filter(Reservation.book_id.in_(
            db.session.query(Book.book_id).filter_by(library_id=user.library_id)
        )).all()
    else:
        reservations = Reservation.query.filter_by(user_id=user.user_id).all()
    return jsonify({
        "reservations": [{
            "reservation_id": str(r.reservation_id),
            "book_id": str(r.book_id),
            "status": r.status,
            "reserved_at": r.reserved_at.isoformat(),
            "expires_at": r.expires_at.isoformat() if r.expires_at else None,
            "confirmed_at": r.confirmed_at.isoformat() if r.confirmed_at else None
        } for r in reservations]
    }), 200

@reservation_bp.route('/<reservation_id>', methods=['PATCH'])
@role_required(['Librarian'])
def update_reservation(reservation_id):
    form = ReservationUpdateForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400
    reservation = Reservation.query.filter_by(reservation_id=reservation_id).first()
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404
    book = Book.query.filter_by(book_id=reservation.book_id).first()
    if reservation.expires_at < datetime.now():
        reservation.status = 'expired'
        book.reserved_copies -= 1
        db.session.commit()
        return jsonify({"error": "Reservation expired"}), 400
    reservation.status = form.status.data
    if form.status.data == 'confirmed':
        reservation.confirmed_at = datetime.now()
    elif form.status.data == 'rejected':
        book.reserved_copies -= 1
        user = User.query.filter_by(user_id=reservation.user_id).first()
        user.reserved_book_ids.remove(book.book_id)
    db.session.commit()
    return jsonify({"message": "Reservation updated"}), 200