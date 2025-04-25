from .. import db
from uuid import uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class Library(db.Model):
    __tablename__ = 'libraries'

    library_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    country = db.Column(db.Text)
    pincode = db.Column(db.BigInteger)
    admin_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    users = db.relationship('User', backref='library', cascade='all, delete', foreign_keys='User.library_id')
    books = db.relationship('Book', backref='library', cascade='all, delete')
    policies = db.relationship('Policy', backref='library', cascade='all, delete')
    fines = db.relationship('Fine', backref='library', cascade='all, delete')
    document_uploads = db.relationship('DocumentUpload', backref='library', cascade='all, delete')

    def __repr__(self):
        return f"<Library {self.name}>"