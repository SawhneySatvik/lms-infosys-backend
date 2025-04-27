from flask import Blueprint

genres_bp = Blueprint('genres', __name__, url_prefix='/genres')

from . import routes