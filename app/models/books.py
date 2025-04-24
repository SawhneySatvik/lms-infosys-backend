from .. import db
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from uuid import uuid4
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    library_id = db.Column(UUID(as_uuid=True), db.ForeignKey('libraries.library_id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    isbn = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)
    publisher_name = db.Column(db.Text)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    reserved_copies = db.Column(db.Integer, default=0)
    book_image = db.Column(db.Text)
    author_ids = db.Column(ARRAY(UUID(as_uuid=True)), default=list)
    genre_ids = db.Column(ARRAY(UUID(as_uuid=True)), default=list)
    published_date = db.Column(db.DateTime)
    added_on = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    borrow_transactions = db.relationship('BorrowTransaction', backref='book', cascade='all, delete')
    reservations = db.relationship('Reservation', backref='book', cascade='all, delete')
    wishlists = db.relationship('Wishlist', backref='book', cascade='all, delete')
    reviews = db.relationship('Review', backref='book', cascade='all, delete')
    fines = db.relationship('Fine', backref='book', cascade='all, delete')
    document_uploads = db.relationship('DocumentUpload', backref='book')

    __table_args__ = (
        db.CheckConstraint('total_copies >= 0', name='check_total_copies'),
        db.CheckConstraint('available_copies >= 0', name='check_available_copies'),
        db.CheckConstraint('reserved_copies >= 0', name='check_reserved_copies'),
    )

    def __repr__(self):
        return f"<Book {self.title}>"