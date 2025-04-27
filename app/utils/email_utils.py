import smtplib
from ..config import Config
from email.message import EmailMessage

def generate_otp(length=6):
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def send_otp_email(email, otp):
    try:
        msg = EmailMessage()
        msg.set_content(f"Your OTP is: {otp}. It is valid for 5 minutes.")
        msg['Subject'] = 'Library Management System OTP'
        msg['From'] = Config.MAIL_USERNAME
        msg['To'] = email

        with smtplib.SMTP_SSL(
            Config.MAIL_SERVER,
            Config.MAIL_PORT
        ) as server:
            server.login(
                Config.MAIL_USERNAME,
                Config.MAIL_PASSWORD
            )
            server.send_message(msg)
        print(f"OTP email sent to {email}: OTP={otp}")
        return True
    except Exception as e:
        print(f"Error sending OTP email to {email}: {str(e)}")
        return False