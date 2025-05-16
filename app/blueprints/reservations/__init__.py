from flask import Blueprint

reservation_bp = Blueprint('reservation', __name__, url_prefix='/reservations')
