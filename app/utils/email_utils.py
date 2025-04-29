import smtplib
from ..config import Config
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import string

def generate_otp(length=6):
    """Generate a random OTP of specified length."""
    return ''.join(secrets.choice(string.digits) for _ in range(length))

def send_otp_email(recipient, body, subject="Your OTP for Library Management System", is_otp=True):
    """Send an email with OTP or custom body to the recipient."""
    try:
        msg = MIMEMultipart()
        msg['From'] = Config.SMTP_SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject

        # If it's an OTP, wrap it in a simple message
        if is_otp:
            email_body = f"Your OTP is: {body}\n\nThis OTP is valid for 5 minutes."
        else:
            email_body = body  # Use the provided body directly

        msg.attach(MIMEText(email_body, 'plain'))

        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_SENDER_EMAIL, Config.SMTP_SENDER_PASSWORD)
            server.sendmail(Config.SMTP_SENDER_EMAIL, recipient, msg.as_string())
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False