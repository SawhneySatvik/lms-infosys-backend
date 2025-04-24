from .. import db
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from uuid import uuid4
from datetime import datetime

class Author(db.Model):
    __tablename__ = 'authors'

    author_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.Text, nullable=False)
    bio = db.Column(db.Text)
    author_image = db.Column(db.Text)
    book_ids = db.Column(ARRAY(UUID(as_uuid=True)), default=list)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Author {self.name}>"