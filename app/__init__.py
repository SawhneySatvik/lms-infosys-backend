from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

from .models import *

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.route('/test-db')
    def test_db():
        try:
            result = db.session.execute(db.text('SELECT * FROM libraries LIMIT 1')).fetchall()
            return {"message": "Database connected", "data": [dict(row._mapping) for row in result]}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    return app