from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Project Secret
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Supabase Project
    SUPABASE_PROJECT_URL = os.getenv('SUPABASE_PROJECT_URL')
    SUPABASE_ANON_PUBLIC_KEY = os.getenv('SUPABASE_ANON_PUBLIC_KEY')
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
    SUPABASE_PROJECT_PASSWORD = os.getenv("SUPABASE_PROJECT_PASSWORD")

    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET")
    ACCESS_TOKEN_EXPIRY_TIME = os.getenv("ACCESS_TOKEN_EXPIRY_TIME")
    
    # Database URI
    DATABASE_URI = os.getenv("DATABASE_URI")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # WTForms
    WTF_CSRF_ENABLED = False

    # Storage
    S3_ENDPOINT = os.getenv("SUPABASE_S3_ENDPOINT")
    S3_REGION = os.getenv("SUPABASE_S3_REGION")

    # Email configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("EMAIL_ID")
    MAIL_PASSWORD = os.getenv("EMAIl_APP_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("EMAIL_ID")