from .. import db
from uuid import uuid4
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = 'reservations'

    reservation_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    library_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('libraries.library_id', ondelete='CASCADE'), nullable=False)
    reserved_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    status = db.Column(db.Text, default='pending')
    confirmed_at = db.Column(db.DateTime)

    __table_args__ = (
        db.CheckConstraint("status IN ('pending', 'confirmed', 'rejected', 'expired')", name='check_status'),
    )

    def __repr__(self):
        return f"<Reservation reservation_id={self.reservation_id}>"