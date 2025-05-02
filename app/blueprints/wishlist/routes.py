from flask import request, jsonify
from . import wishlist_bp
from .forms import WishlistForm
from ... import db
from ...models.books import Book
from ...models.wishlists import Wishlist
from ...utils.role_manager import role_required

@wishlist_bp.route('', methods=['POST'])
@role_required(['Member'])
def add_to_wishlist():
    form = WishlistForm()
    if not form.validate_on_submit():
        return jsonify({"error": form.errors}), 400
    member = request.current_user
    book = Book.query.filter_by(book_id=form.book_id.data, library_id=member.library_id).first()
    if not book:
        return jsonify({"error": "Book not found in library"}), 404
    if Wishlist.query.filter_by(user_id=member.user_id, book_id=book.book_id).first():
        return jsonify({"error": "Book already in wishlist"}), 400
    new_wishlist = Wishlist(user_id=member.user_id, book_id=book.book_id)
    member.wishlist_book_ids.append(book.book_id)
    db.session.add(new_wishlist)
    db.session.commit()
    return jsonify({"message": "Book added to wishlist", "wishlist_id": str(new_wishlist.wishlist_id)}), 201

@wishlist_bp.route('', methods=['GET'])
@role_required(['Member'])
def list_wishlist():
    member = request.current_user
    wishlists = Wishlist.query.filter_by(user_id=member.user_id).all()
    return jsonify({
        "wishlists": [{
            "wishlist_id": str(w.wishlist_id),
            "book_id": str(w.book_id),
            "added_at": w.added_at.isoformat()
        } for w in wishlists]
    }), 200

@wishlist_bp.route('/<wishlist_id>', methods=['DELETE'])
@role_required(['Member'])
def remove_from_wishlist(wishlist_id):
    member = request.current_user
    wishlist = Wishlist.query.filter_by(wishlist_id=wishlist_id, user_id=member.user_id).first()
    if not wishlist:
        return jsonify({"error": "Wishlist item not found"}), 404
    member.wishlist_book_ids.remove(wishlist.book_id)
    db.session.delete(wishlist)
    db.session.commit()
    return jsonify({"message": "Book removed from wishlist"}), 200