from .. import db
from uuid import uuid4
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = 'tickets'

    ticket_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    resolved_by = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.user_id'))
    type = db.Column(db.Text, nullable=False)
    subject = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, default='open')
    priority = db.Column(db.Text, default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

    __table_args__ = (
        db.CheckConstraint("status IN ('open', 'in_progress', 'resolved')", name='check_status'),
        db.CheckConstraint("priority IN ('low', 'medium', 'high')", name='check_priority'),
    )

    def __repr__(self):
        return f"<Ticket ticket_id={self.ticket_id}>"