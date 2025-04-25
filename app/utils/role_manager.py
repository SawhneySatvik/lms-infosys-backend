from functools import wraps
from flask import request, jsonify, current_app
import jwt
from .. import db
from ..models.users import User
from ..config import Config

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get JWT from Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Missing or invalid Authorization header"}), 401

            token = auth_header.split(" ")[1]
            print(f"Received token: {token[:10]}...")  # Debug: Print first 10 chars

            try:
                # Decode JWT with Supabase JWT secret
                decoded = jwt.decode(
                    token,
                    Config.JWT_SECRET,
                    algorithms=["HS256"],
                    options={"verify_aud": False, "verify_iss": False}
                )
                user_id = decoded.get('sub')
                print(f"Decoded user_id: {user_id}")  # Debug

                if not user_id:
                    return jsonify({"error": "Invalid token: user_id not found"}), 401

                # Query users table for role
                user = User.query.filter_by(user_id=user_id, is_active=True).first()
                print(f"User found: {user.email if user else 'None'}")  # Debug
                if not user:
                    return jsonify({"error": "User not found or inactive"}), 404

                # Check if user's role is allowed
                print(f"User role: {user.role}, Allowed roles: {allowed_roles}")  # Debug
                if user.role not in allowed_roles:
                    return jsonify({"error": f"Unauthorized: {user.role} not allowed"}), 403

                # Store user in request context
                request.current_user = user

            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401
            except jwt.InvalidTokenError as e:
                print(f"Invalid token error: {str(e)}")  # Debug
                return jsonify({"error": "Invalid token"}), 401
            except Exception as e:
                print(f"Server error: {str(e)}")  # Debug
                return jsonify({"error": f"Server error: {str(e)}"}), 500

            return f(*args, **kwargs)
        return decorated_function
    return decorator