from flask import request, jsonify, current_app
from . import auth_bp
from .forms import SignupForm, LoginForm, ProfileForm, ResetPasswordForm, RefreshTokenForm, AdminRegisterForm, LibrarianRegisterForm
from ... import db
from ...models.users import User
from ...models.libraries import Library
from ...config import Config
from supabase import create_client, Client
from ...utils.role_manager import role_required
from datetime import datetime

# Initialize Supabase client
supabase: Client = create_client(Config.SUPABASE_PROJECT_URL, Config.SUPABASE_ANON_PUBLIC_KEY)
supabase_admin: Client = create_client(Config.SUPABASE_PROJECT_URL, Config.SUPABASE_SERVICE_KEY)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
                filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
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
            # Create library without admin_id
            new_library = Library(
                name=form.library_name.data,
                address=form.address.data,
                city=form.city.data,
                state=form.state.data,
                country=form.country.data,
                pincode=form.pincode.data,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(new_library)
            db.session.flush()  # Generate library_id

            library_id = new_library.library_id

            # Create user
            new_user = User(
                user_id=user_id,
                library_id=library_id,
                name=form.name.data,
                email=form.email.data,
                role='Admin',
                is_active=True,
                user_image=user_image_url,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.flush()  # Persist user to users table

            # Update library with admin_id
            new_library.admin_id = user_id
            db.session.add(new_library)

            db.session.commit()
        except Exception as e:
            try:
                supabase_admin.auth.admin.delete_user(user_id)
            except Exception as delete_error:
                pass
            db.session.rollback()
            return jsonify({"error": f"Failed to create admin or library: {str(e)}"}), 500

        return jsonify({
            "message": "Admin registered successfully. You can now sign in.",
            "user_id": str(user_id),
            "library_id": str(library_id)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@auth_bp.route('/librarian/register', methods=['POST'])
@role_required(['Admin'])
def librarian_register():
    form = LibrarianRegisterForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        # Get admin's library_id
        admin = request.current_user
        library = Library.query.filter_by(library_id=admin.library_id).first()
        if not library:
            return jsonify({"error": "Admin's library not found"}), 404

        # Upload user_image if provided
        user_image_url = None
        if 'user_image' in request.files:
            file = request.files['user_image']
            if file and allowed_file(file.filename):
                filename = f"{datetime.now().timestamp()}_{file.filename}"
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
            "options": {"data": {"role": "Librarian"}}
        })
        user_id = auth_response.user.id

        # Create user in users table
        try:
            new_user = User(
                user_id=user_id,
                library_id=admin.library_id,
                name=form.name.data,
                email=form.email.data,
                role='Librarian',
                is_active=True,
                user_image=user_image_url,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            try:
                supabase_admin.auth.admin.delete_user(user_id)
            except Exception as delete_error:
                pass
            db.session.rollback()
            return jsonify({"error": f"Failed to create librarian: {str(e)}"}), 500

        return jsonify({
            "message": "Librarian registered successfully. They can now sign in.",
            "user_id": str(user_id)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@auth_bp.route('/signup', methods=['POST'])
def signup():
    form = SignupForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        library = Library.query.filter_by(library_id=form.library_id.data).first()
        if not library:
            return jsonify({"error": "Invalid library_id"}), 400

        if User.query.filter_by(email=form.email.data).first():
            return jsonify({"error": "Email already registered"}), 400

        user_image_url = None
        if 'user_image' in request.files:
            file = request.files['user_image']
            if file and allowed_file(file.filename):
                filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
                supabase.storage.from_('user_images').upload(
                    path=filename,
                    file=file.stream,
                    file_options={"content-type": file.content_type}
                )
                user_image_url = supabase.storage.from_('user_images').get_public_url(filename)

        auth_response = supabase.auth.sign_up({
            "email": form.email.data,
            "password": form.password.data
        })
        user_id = auth_response.user.id

        try:
            new_user = User(
                user_id=user_id,
                library_id=form.library_id.data,
                name=form.name.data,
                email=form.email.data,
                role='Member',
                is_active=True,
                user_image=user_image_url,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            try:
                supabase_admin.auth.admin.delete_user(user_id)
            except Exception as delete_error:
                pass
            db.session.rollback()
            return jsonify({"error": f"Failed to create user: {str(e)}"}), 500

        return jsonify({
            "message": "User registered successfully. You can now sign in.",
            "user_id": str(user_id)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@auth_bp.route('/signin', methods=['POST'])
def signin():
    form = LoginForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        response = supabase.auth.sign_in_with_password({
            "email": form.email.data,
            "password": form.password.data
        })
        user_id = response.user.id

        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        access_token = response.session.access_token
        refresh_token = response.session.refresh_token

        return jsonify({
            "message": "Signed in successfully",
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
        return jsonify({"error": "Invalid credentials or server error"}), 401

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    form = RefreshTokenForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        response = supabase.auth.refresh_session(form.refresh_token.data)
        access_token = response.session.access_token
        new_refresh_token = response.session.refresh_token

        user = User.query.filter_by(user_id=response.user.id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

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
        supabase.auth.sign_out()
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Logout failed: {str(e)}"}), 500

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
            user_image_url = user.user_image
            if 'user_image' in request.files:
                file = request.files['user_image']
                if file and allowed_file(file.filename):
                    filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
                    supabase.storage.from_('user_images').upload(
                        path=filename,
                        file=file.stream,
                        file_options={"content-type": file.content_type}
                    )
                    user_image_url = supabase.storage.from_('user_images').get_public_url(filename)

            if form.name.data:
                user.name = form.name.data
            if user_image_url and user_image_url != user.user_image:
                user.user_image = user_image_url
            user.updated_at = datetime.utcnow()
            db.session.commit()

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
            return jsonify({"error": f"Profile update failed: {str(e)}"}), 400

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    form = ResetPasswordForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        supabase.auth.reset_password_for_email(form.email.data)
        return jsonify({"message": "Password reset email sent"}), 200
    except Exception as e:
        return jsonify({"error": f"Password reset failed: {str(e)}"}), 400