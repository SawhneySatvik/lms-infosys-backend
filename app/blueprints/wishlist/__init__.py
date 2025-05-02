from flask import Blueprint

wishlist_bp = Blueprint('wishlist', __name__, url_prefix='/wishlist')

from . import routes