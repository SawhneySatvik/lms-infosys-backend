from flask import request, jsonify
from . import ticket_bp
from datetime import datetime
from .forms import TicketForm, TicketUpdateForm
from ... import db
from ...models.users import User
from ...models.tickets import Ticket
from ...utils.role_manager import role_required

@ticket_bp.route('', methods=['POST'])
@role_required(['Librarian'])
def create_ticket():
    form = TicketForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400
    librarian = request.current_user
    ticket = Ticket(
        user_id=librarian.user_id,
        type=form.type.data,
        subject=form.subject.data,
        message=form.message.data,
        priority=form.priority.data or 'medium',
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.session.add(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket created", "ticket_id": str(ticket.ticket_id)}), 201

@ticket_bp.route('', methods=['GET'])
@role_required(['Admin', 'Librarian'])
def list_tickets():
    user = request.current_user
    if user.role == 'Admin':
        tickets = Ticket.query.filter(Ticket.user_id.in_(
            db.session.query(User.user_id).filter_by(library_id=user.library_id, role='Librarian')
        )).all()
    else:
        tickets = Ticket.query.filter_by(user_id=user.user_id).all()
    return jsonify({
        "tickets": [{
            "ticket_id": str(t.ticket_id),
            "subject": t.subject,
            "status": t.status,
            "priority": t.priority,
            "created_at": t.created_at.isoformat(),
            "resolved_at": t.resolved_at.isoformat() if t.resolved_at else None
        } for t in tickets]
    }), 200

@ticket_bp.route('/<ticket_id>', methods=['PATCH'])
@role_required(['Admin'])
def update_ticket(ticket_id):
    form = TicketUpdateForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    ticket.status = form.status.data
    ticket.resolved_by = request.current_user.user_id if form.status.data == 'resolved' else None
    ticket.resolved_at = datetime.now() if form.status.data == 'resolved' else None
    ticket.updated_at = datetime.now()
    db.session.commit()
    return jsonify({"message": "Ticket updated"}), 200