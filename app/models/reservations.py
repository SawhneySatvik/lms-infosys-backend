from .. import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = 'reservations'

    reservation_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    reserved_at = db.Column(db.DateTime, default=datetime.now)
    expires_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Reservation reservation_id={self.reservation_id}>"