from .. import db
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(UUID(as_uuid=True), primary_key=True)  # References auth.users.id
    library_id = db.Column(UUID(as_uuid=True), db.ForeignKey('libraries.library_id', ondelete='CASCADE'), nullable=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    role = db.Column(db.Text, nullable=False, server_default='Member')
    is_active = db.Column(db.Boolean, default=False)  # Changed default to match registration flow
    user_image = db.Column(db.Text)
    preferred_genre_ids = db.Column(ARRAY(UUID(as_uuid=True)), default=list)
    borrowed_book_ids = db.Column(ARRAY(UUID(as_uuid=True)), default=list)
    reserved_book_ids = db.Column(ARRAY(UUID(as_uuid=True)), default=list)
    wishlist_book_ids = db.Column(ARRAY(UUID(as_uuid=True)), default=list)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    borrow_transactions = db.relationship('BorrowTransaction', backref='user', cascade='all, delete')
    reservations = db.relationship('Reservation', backref='user', cascade='all, delete')
    wishlists = db.relationship('Wishlist', backref='user', cascade='all, delete')
    reviews = db.relationship('Review', backref='user', cascade='all, delete')
    tickets = db.relationship('Ticket', foreign_keys='Ticket.user_id', backref='user', cascade='all, delete')
    resolved_tickets = db.relationship('Ticket', foreign_keys='Ticket.resolved_by', backref='resolver')
    fines = db.relationship('Fine', backref='user', cascade='all, delete')
    document_uploads = db.relationship('DocumentUpload', backref='user', cascade='all, delete')

    __table_args__ = (
        db.CheckConstraint("role IN ('Admin', 'Librarian', 'Member')", name='check_role'),
    )

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"