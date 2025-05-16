from flask import request, jsonify
from datetime import datetime
from . import fine_bp
from .forms import FineForm, FineUpdateForm
from ... import db
from ...models.fines import Fine
from ...models.borrow_transactions import BorrowTransaction
from ...utils.role_manager import role_required

@fine_bp.route('', methods=['GET'])
@role_required(['Librarian', 'Member'])
def list_fines():
    user = request.current_user
    fines = Fine.query.filter_by(
        user_id=user.user_id if user.role == 'Member' else None,
        library_id=user.library_id
    ).all()
    return jsonify({
        "fines": [{
            "fine_id": str(f.fine_id),
            "amount": float(f.amount),
            "reason": f.reason,
            "is_paid": f.is_paid,
            "fine_date": f.fine_date.isoformat(),
            "paid_at": f.paid_at.isoformat() if f.paid_at else None
        } for f in fines]
    }), 200

@fine_bp.route('', methods=['POST'])
@role_required(['Librarian'])
def create_fine():
    form = FineForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400
    borrow = BorrowTransaction.query.filter_by(borrow_id=form.borrow_id.data).first()
    if not borrow:
        return jsonify({"error": "Borrow transaction not found"}), 404
    fine = Fine(
        borrow_id=borrow.borrow_id,
        user_id=borrow.user_id,
        book_id=borrow.book_id,
        library_id=borrow.library_id,
        amount=form.amount.data,
        reason=form.reason.data,
        fine_date=datetime.now()
    )
    db.session.add(fine)
    db.session.commit()
    return jsonify({"message": "Fine created", "fine_id": str(fine.fine_id)}), 201

@fine_bp.route('/<fine_id>', methods=['PATCH'])
@role_required(['Member'])
def pay_fine(fine_id):
    form = FineUpdateForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400
    fine = Fine.query.filter_by(fine_id=fine_id, user_id=request.current_user.user_id).first()
    if not fine:
        return jsonify({"error": "Fine not found"}), 404
    fine.is_paid = form.is_paid.data if form.is_paid.data is not None else fine.is_paid
    fine.paid_at = datetime.now() if fine.is_paid else None
    fine.updated_at = datetime.now()
    db.session.commit()
    return jsonify({"message": "Fine updated"}), 200