import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import secrets
from flask import current_app

load_dotenv()

def generate_otp(length=6):
    """Generate a secure 6-digit OTP."""
    return ''.join(secrets.choice('0123456789') for _ in range(length))

def send_otp_email(receiver_email, otp):
    """Send OTP email using Gmail SMTP."""
    sender_email = os.getenv('EMAIL_ID')
    sender_password = os.getenv('EMAIL_APP_PASSWORD')

    subject = "Your LMS OTP Verification Code"
    body = (
        '<div style="font-family: Arial, sans-serif; text-align: center;">'
        '<h2>Your OTP Code</h2>'
        f'<p>Your OTP code is <strong>{otp}</strong>. It expires in 5 minutes.</p>'
        '<p>© 2025 Library Management System</p>'
        '</div>'
    )

    msg = EmailMessage()
    msg.set_content(body, subtype='html')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        current_app.logger.info(f"OTP sent to {receiver_email}")
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending OTP email to {receiver_email}: {str(e)}")
        return False
