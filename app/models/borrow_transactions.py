from .. import db
from uuid import uuid4
from datetime import datetime

class BorrowTransaction(db.Model):
    __tablename__ = 'borrow_transactions'

    borrow_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    library_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('libraries.library_id', ondelete='CASCADE'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.Text, default='borrowed')

    fines = db.relationship('Fine', backref='borrow_transaction', cascade='all, delete')

    __table_args__ = (
        db.CheckConstraint("status IN ('borrowed', 'returned', 'overdue')", name='check_status'),
    )

    def __repr__(self):
        return f"<BorrowTransaction borrow_id={self.borrow_id}>"