from flask import Blueprint

ticket_bp = Blueprint('ticket', __name__, url_prefix='/tickets')

from . import routes