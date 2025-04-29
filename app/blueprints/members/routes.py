from flask import request, jsonify
from . import members_bp
from .forms import MemberUpdateForm
from ... import db
from ...models.users import User
from ...utils.role_manager import role_required
from datetime import datetime

@members_bp.route('', methods=['GET'])
@role_required(['Admin', 'Librarian'])
def list_members():
    try:
        user = request.current_user
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        members = User.query.filter_by(library_id=user.library_id, role='Member').paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({
            "members": [{
                "user_id": str(member.user_id),
                "name": member.name,
                "email": member.email,
                "is_active": member.is_active
            } for member in members.items],
            "total": members.total,
            "pages": members.pages,
            "page": page
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to list members: {str(e)}"}), 500

@members_bp.route('/<member_id>', methods=['GET'])
@role_required(['Admin', 'Librarian'])
def get_member(member_id):
    try:
        user = request.current_user
        member = User.query.filter_by(user_id=member_id, library_id=user.library_id, role='Member').first()
        if not member:
            return jsonify({"error": "Member not found"}), 404
        return jsonify({
            "user_id": str(member.user_id),
            "name": member.name,
            "email": member.email,
            "is_active": member.is_active
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to get member: {str(e)}"}), 500

@members_bp.route('/<member_id>', methods=['PATCH'])
@role_required(['Admin', 'Librarian'])
def update_member(member_id):
    form = MemberUpdateForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400

    try:
        user = request.current_user
        member = User.query.filter_by(user_id=member_id, library_id=user.library_id, role='Member').first()
        if not member:
            return jsonify({"error": "Member not found"}), 404

        if form.name.data:
            member.name = form.name.data
        if form.email.data:
            member.email = form.email.data
        if form.is_active.data is not None:
            member.is_active = form.is_active.data
        member.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify({"message": "Member updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update member: {str(e)}"}), 500

@members_bp.route('/<member_id>', methods=['DELETE'])
@role_required(['Admin', 'Librarian'])
def delete_member(member_id):
    try:
        user = request.current_user
        member = User.query.filter_by(user_id=member_id, library_id=user.library_id, role='Member').first()
        if not member:
            return jsonify({"error": "Member not found"}), 404

        db.session.delete(member)
        db.session.commit()
        return jsonify({"message": "Member deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete member: {str(e)}"}), 500