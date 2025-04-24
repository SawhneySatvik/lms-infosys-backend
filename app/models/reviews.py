from .. import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'

    review_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    reviewed_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        db.CheckConstraint('rating BETWEEN 1 AND 5', name='check_rating'),
    )

    def __repr__(self):
        return f"<Review review_id={self.review_id}>"