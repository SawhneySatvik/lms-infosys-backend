from .. import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = 'tickets'

    ticket_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    resolved_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'))
    type = db.Column(db.Text, nullable=False)
    subject = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, default='open')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        db.CheckConstraint("status IN ('open', 'in_progress', 'resolved')", name='check_status'),
    )

    def __repr__(self):
        return f"<Ticket ticket_id={self.ticket_id}>"