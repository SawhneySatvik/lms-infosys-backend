from flask import request, jsonify
from . import borrowing_bp
from datetime import datetime, timedelta
from .forms import BorrowForm, ReturnForm
from ... import db
from ...models.books import Book
from ...models.borrow_transactions import BorrowTransaction
from ...models.fines import Fine
from ...models.policies import Policy
from ...models.reservations import Reservation
from ...models.users import User
from ...utils.role_manager import role_required

@borrowing_bp.route('', methods=['POST'])
@role_required(['Librarian'])
def borrow_book():
    form = BorrowForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400
    reservation = Reservation.query.filter_by(reservation_id=form.reservation_id.data, status='confirmed').first()
    if not reservation:
        return jsonify({"error": "Confirmed reservation not found"}), 404
    member = User.query.filter_by(user_id=reservation.user_id).first()
    book = Book.query.filter_by(book_id=reservation.book_id).first()
    policy = Policy.query.filter_by(library_id=member.library_id).first()
    if not policy:
        return jsonify({"error": "Library policy not found"}), 404
    if len(member.borrowed_book_ids) >= policy.max_books_per_user:
        return jsonify({"error": "Maximum borrow limit reached"}), 400
    borrow = BorrowTransaction(
        user_id=reservation.user_id,
        book_id=reservation.book_id,
        library_id=member.library_id,
        borrow_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=policy.max_borrow_days),
        status='borrowed'
    )
    book.available_copies -= 1
    book.reserved_copies -= 1
    member.borrowed_book_ids.append(reservation.book_id)
    member.reserved_book_ids.remove(reservation.book_id)
    db.session.delete(reservation)
    db.session.add(borrow)
    db.session.commit()
    return jsonify({"message": "Book borrowed", "borrow_id": str(borrow.borrow_id)}), 201

@borrowing_bp.route('/<borrow_id>', methods=['PATCH'])
@role_required(['Librarian'])
def return_book(borrow_id):
    form = ReturnForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400
    borrow = BorrowTransaction.query.filter_by(borrow_id=borrow_id).first()
    if not borrow or borrow.status != 'borrowed':
        return jsonify({"error": "Invalid borrow transaction"}), 404
    policy = Policy.query.filter_by(library_id=borrow.library_id).first()
    if not policy:
        return jsonify({"error": "Library policy not found"}), 404
    borrow.return_date = datetime.now()
    borrow.status = 'returned' if borrow.return_date <= borrow.due_date else 'overdue'
    book = Book.query.filter_by(book_id=borrow.book_id).first()
    book.available_copies += 1
    member = User.query.filter_by(user_id=borrow.user_id).first()
    member.borrowed_book_ids.remove(borrow.book_id)
    if borrow.status == 'overdue':
        days_late = (borrow.return_date - borrow.due_date).days
        fine_amount = days_late * policy.fine_per_day
        fine = Fine(
            borrow_id=borrow.borrow_id,
            user_id=borrow.user_id,
            book_id=borrow.book_id,
            library_id=member.library_id,
            amount=fine_amount,
            reason='Overdue book return'
        )
        db.session.add(fine)
    db.session.commit()
    return jsonify({"message": "Book returned"}), 200