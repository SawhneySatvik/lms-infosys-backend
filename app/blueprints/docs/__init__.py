from flask import Blueprint

docs_bp = Blueprint('docs', __name__, url_prefix='/docs')

from . import routes