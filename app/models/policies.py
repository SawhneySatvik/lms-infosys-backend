from .. import db
from uuid import uuid4
from datetime import datetime

class Policy(db.Model):
    __tablename__ = 'policies'

    policy_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    library_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('libraries.library_id', ondelete='CASCADE'), nullable=False)
    max_borrow_days = db.Column(db.Integer, nullable=False)
    fine_per_day = db.Column(db.Numeric(6, 2), nullable=False)
    max_books_per_user = db.Column(db.Integer, nullable=False)
    reservation_expiry_hours = db.Column(db.Integer, nullable=False, default=24)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint('max_borrow_days > 0', name='check_max_borrow_days'),
        db.CheckConstraint('fine_per_day >= 0', name='check_fine_per_day'),
        db.CheckConstraint('max_books_per_user > 0', name='check_max_books_per_user'),
        db.CheckConstraint('reservation_expiry_hours > 0', name='check_reservation_expiry_hours'),
    )

    def __repr__(self):
        return f"<Policy library_id={self.library_id}>"