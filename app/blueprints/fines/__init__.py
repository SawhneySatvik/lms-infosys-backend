from flask import Blueprint

fine_bp = Blueprint('fine', __name__, url_prefix='/fines')

from . import routes