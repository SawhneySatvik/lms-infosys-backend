from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

from .models import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('docs.index'))

    @app.route('/health')
    def health():
        return {"message":"I am healthy!"}
    
    @app.route('/test-db')
    def test_db():
        try:
            result = db.session.execute(db.text('SELECT * FROM libraries LIMIT 1')).fetchall()
            return {"message": "Database connected", "data": [dict(row._mapping) for row in result]}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    
    from .blueprints.docs import docs_bp
    from .blueprints.auth import auth_bp
    from .blueprints.books import books_bp
    from .blueprints.authors import authors_bp
    from .blueprints.genres import genres_bp
    from .blueprints.members import members_bp
    from .blueprints.librarians import librarians_bp
    from .blueprints.admin import admin_bp
    # from .blueprints.borrowing import borrowing_bp
    # from .blueprints.fines import fine_bp
    # from .blueprints.reservations import reservation_bp
    # from .blueprints.tickets import ticket_bp
    from .blueprints.wishlist import wishlist_bp

    app.register_blueprint(docs_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(genres_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(librarians_bp)
    app.register_blueprint(admin_bp)
    # app.register_blueprint(borrowing_bp)
    # app.register_blueprint(fine_bp)
    # app.register_blueprint(reservation_bp)
    # app.register_blueprint(ticket_bp)
    app.register_blueprint(wishlist_bp)

    return app