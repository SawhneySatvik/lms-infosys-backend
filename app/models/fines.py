from .. import db
from uuid import uuid4
from datetime import datetime

class Fine(db.Model):
    __tablename__ = 'fines'

    fine_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    borrow_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('borrow_transactions.borrow_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    library_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('libraries.library_id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Numeric(8, 2), nullable=False)
    reason = db.Column(db.Text)
    is_paid = db.Column(db.Boolean, default=False)
    fine_date = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint('amount >= 0', name='check_amount'),
    )

    def __repr__(self):
        return f"<Fine fine_id={self.fine_id}>"