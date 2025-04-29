from flask import Blueprint

librarians_bp = Blueprint('librarians', __name__, url_prefix='/librarians')

from . import routes