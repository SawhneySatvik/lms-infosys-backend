from flask import request, jsonify, current_app
from .. import auth_bp
from .forms import SignupForm, LoginForm, OTPForm, ProfileForm, ResetPasswordForm, RefreshTokenForm, AdminRegisterForm
from ... import db
from ...models.users import User
from ...models.libraries import Library
from ...models.otp_verifications import OTPVerification
from ...config import Config
from supabase import create_client, Client
from ...utils.role_manager import role_required
from ...utils.email_utils import generate_otp, send_otp_email
import uuid
from datetime import datetime, timedelta

# Initialize Supabase client
supabase: Client = create_client(Config.SUPABASE_PROJECT_URL, Config.SUPABASE_ANON_PUBLIC_KEY)

@auth_bp.route('/admin/register', methods=['POST'])
def admin_register():
    form = AdminRegisterForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        # Upload user_image if provided
        user_image_url = None
        if 'user_image' in request.files:
            file = request.files['user_image']
            if file and allowed_file(file.filename):
                filename = f"{uuid.uuid4()}_{file.filename}"
                # Upload to Supabase Storage (user_images bucket)
                supabase.storage.from_('user_images').upload(
                    path=filename,
                    file=file.stream,
                    file_options={"content-type": file.content_type}
                )
                user_image_url = supabase.storage.from_('user_images').get_public_url(filename)

        # Create user in auth.users
        auth_response = supabase.auth.sign_up({
            "email": form.email.data,
            "password": form.password.data,
            "options": {"data": {"role": "Admin"}}
        })
        user_id = auth_response.user.id

        # Create library and user in a transaction
        try:
            # Create library
            library_id = uuid.uuid4()
            new_library = Library(
                library_id=library_id,
                name=form.library_name.data,
                address=form.address.data,
                city=form.city.data,
                state=form.state.data,
                country=form.country.data,
                pincode=form.pincode.data,
                admin_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(new_library)

            # Create user
            new_user = User(
                user_id=user_id,
                library_id=library_id,
                name=form.name.data,
                email=form.email.data,
                role='Admin',
                is_active=False,  # Pending OTP verification
                user_image=user_image_url,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            # Rollback auth.users creation if library or user fails
            supabase.auth.admin.delete_user(user_id)
            db.session.rollback()
            return jsonify({"error": f"Failed to create admin or library: {str(e)}"}), 500

        # Generate and send OTP
        otp = generate_otp()  # 6-digit OTP
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        otp_record = OTPVerification(
            user_id=user_id,
            email=form.email.data,
            otp=otp,
            expires_at=expires_at
        )
        db.session.add(otp_record)
        db.session.commit()

        # Send OTP email
        if not send_otp_email(form.email.data, otp):
            db.session.rollback()
            supabase.auth.admin.delete_user(user_id)
            db.session.delete(new_library)
            return jsonify({"error": "Failed to send OTP email"}), 500

        return jsonify({
            "message": "Admin registered. Please verify OTP sent to your email.",
            "user_id": str(user_id)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/signup', methods=['POST'])
def signup():
    form = SignupForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        # Check if library_id exists
        library = Library.query.filter_by(library_id=form.library_id.data).first()
        if not library:
            return jsonify({"error": "Invalid library_id"}), 400

        # Check if email is already registered
        if User.query.filter_by(email=form.email.data).first():
            return jsonify({"error": "Email already registered"}), 400

        # Upload user_image if provided
        user_image_url = None
        if 'user_image' in request.files:
            file = request.files['user_image']
            if file and allowed_file(file.filename):
                filename = f"{uuid.uuid4()}_{file.filename}"
                # Upload to Supabase Storage (user_images bucket)
                supabase.storage.from_('user_images').upload(
                    path=filename,
                    file=file.stream,
                    file_options={"content-type": file.content_type}
                )
                user_image_url = supabase.storage.from_('user_images').get_public_url(filename)

        # Create user in auth.users
        auth_response = supabase.auth.sign_up({
            "email": form.email.data,
            "password": form.password.data
        })
        user_id = auth_response.user.id

        # Create user in users table (pending 2FA)
        try:
            new_user = User(
                user_id=user_id,
                library_id=form.library_id.data,
                name=form.name.data,
                email=form.email.data,
                role='Member',
                is_active=False,  # Pending OTP verification
                user_image=user_image_url,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            # Rollback auth.users creation if users table fails
            supabase.auth.admin.delete_user(user_id)
            db.session.rollback()
            return jsonify({"error": f"Failed to create user: {str(e)}"}), 500

        # Generate and send OTP
        otp = generate_otp()  # 6-digit OTP
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        otp_record = OTPVerification(
            user_id=user_id,
            email=form.email.data,
            otp=otp,
            expires_at=expires_at
        )
        db.session.add(otp_record)
        db.session.commit()

        # Send OTP email
        if not send_otp_email(form.email.data, otp):
            db.session.rollback()
            supabase.auth.admin.delete_user(user_id)
            return jsonify({"error": "Failed to send OTP email"}), 500

        return jsonify({
            "message": "User registered. Please verify OTP sent to your email.",
            "user_id": str(user_id)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/signin', methods=['POST'])
def signin():
    form = LoginForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        # Authenticate with Supabase
        response = supabase.auth.sign_in_with_password({
            "email": form.email.data,
            "password": form.password.data
        })
        user_id = response.user.id

        # Check if user exists and is active
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        if not user.is_active:
            return jsonify({"error": "Account not activated. Please verify OTP from signup."}), 403

        # Generate and send OTP
        otp = generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        otp_record = OTPVerification(
            user_id=user_id,
            email=form.email.data,
            otp=otp,
            expires_at=expires_at
        )
        db.session.add(otp_record)
        db.session.commit()

        # Send OTP email
        if not send_otp_email(form.email.data, otp):
            db.session.rollback()
            return jsonify({"error": "Failed to send OTP email"}), 500

        return jsonify({
            "message": "Please verify OTP sent to your email.",
            "user_id": str(user_id)
        }), 200

    except Exception as e:
        return jsonify({"error": "Invalid credentials or server error"}), 401

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    form = OTPForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        # Find OTP record
        otp_record = OTPVerification.query.filter_by(
            user_id=form.user_id.data,
            otp=form.otp.data
        ).first()

        flow = form.flow.data or "unknown"
        if not otp_record:
            error_msg = f"Invalid OTP or user_id for {flow} verification"
            return jsonify({"error": error_msg}), 400
        if otp_record.expires_at < datetime.utcnow():
            db.session.delete(otp_record)
            db.session.commit()
            return jsonify({"error": f"OTP expired for {flow} verification"}), 400

        # Validate user
        user = User.query.filter_by(user_id=form.user_id.data).first()
        if not user:
            return jsonify({"error": f"User not found for {flow} verification"}), 404

        # Flow-specific checks
        if flow == "signup" and user.is_active:
            return jsonify({"error": "Account already activated"}), 400
        if flow == "signin" and not user.is_active:
            return jsonify({"error": "Account not activated. Please verify signup OTP first."}), 403

        # Activate user for signup flow
        if not user.is_active:
            user.is_active = True
            user.updated_at = datetime.utcnow()
            db.session.commit()

        # Sign in to get JWT and refresh token
        login_response = supabase.auth.sign_in_with_password({
            "email": otp_record.email,
            "password": None  # OTP verification bypasses password
        })
        access_token = login_response.session.access_token
        refresh_token = login_response.session.refresh_token

        # Delete OTP record
        db.session.delete(otp_record)
        db.session.commit()

        return jsonify({
            "message": f"OTP verified successfully for {flow}",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "user_id": str(user.user_id),
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "user_image": user.user_image
            }
        }), 200

    except Exception as e:
        error_msg = f"Error verifying OTP for {form.flow.data or 'unknown'}: {str(e)}"
        return jsonify({"error": error_msg}), 400

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    form = RefreshTokenForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        # Refresh session with Supabase
        response = supabase.auth.refresh_session(form.refresh_token.data)
        access_token = response.session.access_token
        new_refresh_token = response.session.refresh_token

        # Get user details
        user = User.query.filter_by(user_id=response.user.id, is_active=True).first()
        if not user:
            return jsonify({"error": "User not found or inactive"}), 404

        return jsonify({
            "message": "Token refreshed successfully",
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "user": {
                "user_id": str(user.user_id),
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "user_image": user.user_image
            }
        }), 200

    except Exception as e:
        return jsonify({"error": "Invalid refresh token or server error"}), 401

@auth_bp.route('/signout', methods=['POST'])
@role_required(['Member', 'Librarian', 'Admin'])
def signout():
    try:
        # Supabase handles session invalidation
        supabase.auth.sign_out()
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/profile', methods=['GET', 'PATCH'])
@role_required(['Member', 'Librarian', 'Admin'])
def profile():
    user = request.current_user

    if request.method == 'GET':
        return jsonify({
            "user": {
                "user_id": str(user.user_id),
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "library_id": str(user.library_id),
                "user_image": user.user_image
            }
        }), 200

    if request.method == 'PATCH':
        form = ProfileForm()
        if not form.validate_on_submit():
            return jsonify({"error": form.errors}), 400

        try:
            # Update user_image if provided
            user_image_url = user.user_image
            if 'user_image' in request.files:
                file = request.files['user_image']
                if file and allowed_file(file.filename):
                    filename = f"{uuid.uuid4()}_{file.filename}"
                    supabase.storage.from_('user_images').upload(
                        path=filename,
                        file=file.stream,
                        file_options={"content-type": file.content_type}
                    )
                    user_image_url = supabase.storage.from_('user_images').get_public_url(filename)

            # Update users table
            if form.name.data:
                user.name = form.name.data
            if user_image_url and user_image_url != user.user_image:
                user.user_image = user_image_url
            user.updated_at = datetime.utcnow()
            db.session.commit()

            # Update email in auth.users if provided
            if form.email.data and form.email.data != user.email:
                supabase.auth.update_user({"email": form.email.data})
                user.email = form.email.data
                db.session.commit()

            return jsonify({
                "message": "Profile updated successfully",
                "user": {
                    "user_id": str(user.user_id),
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "user_image": user.user_image
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    form = ResetPasswordForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        # Initiate password reset
        supabase.auth.reset_password_for_email(form.email.data)
        return jsonify({"message": "Password reset email sent"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS