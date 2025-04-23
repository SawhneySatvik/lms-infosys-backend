from dotenv import load_dotenv
import os

load_dotenv()

class Config:
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

    # Storage
    S3_ENDPOINT = os.getenv("SUPABASE_S3_ENDPOINT")
    S3_REGION = os.getenv("SUPABASE_S3_REGION")