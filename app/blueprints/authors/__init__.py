from flask import Blueprint

authors_bp = Blueprint('authors', __name__, url_prefix='/authors')

from . import routes