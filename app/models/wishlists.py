from .. import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime

class Wishlist(db.Model):
    __tablename__ = 'wishlists'

    wishlist_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id', name='uq_wishlist_user_book'),
    )

    def __repr__(self):
        return f"<Wishlist wishlist_id={self.wishlist_id}>"