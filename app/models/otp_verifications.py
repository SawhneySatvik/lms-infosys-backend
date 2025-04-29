from .. import db
from datetime import datetime, timezone
import uuid

class OTPVerification(db.Model):
    __tablename__ = 'otp_verifications'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    email = db.Column(db.Text, nullable=False)
    otp = db.Column(db.Text, nullable=False)
    access_token = db.Column(db.Text, nullable=True)  # Added for login tokens
    refresh_token = db.Column(db.Text, nullable=True)  # Added for login tokens
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<OTPVerification user_id={self.user_id}, email={self.email}, otp={self.otp}, expires_at={self.expires_at}>"