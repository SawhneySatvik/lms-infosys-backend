import smtplib
from email.message import EmailMessage
from flask import current_app
from . import logger

def generate_otp(length=6):
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def send_otp_email(email, otp):
    try:
        msg = EmailMessage()
        msg.set_content(f"Your OTP is: {otp}. It is valid for 5 minutes.")
        msg['Subject'] = 'Library Management System OTP'
        msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
        msg['To'] = email

        with smtplib.SMTP_SSL(
            current_app.config['MAIL_SERVER'],
            current_app.config['MAIL_PORT']
        ) as server:
            server.login(
                current_app.config['MAIL_USERNAME'],
                current_app.config['MAIL_PASSWORD']
            )
            server.send_message(msg)
        logger.debug(f"OTP email sent to {email}: OTP={otp}")
        return True
    except Exception as e:
        logger.error(f"Error sending OTP email to {email}: {str(e)}")
        return False