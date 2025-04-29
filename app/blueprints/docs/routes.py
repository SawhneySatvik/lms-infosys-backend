from flask import render_template
from . import docs_bp

@docs_bp.route('/')
def index():
    # Static example data — you can generate this dynamically if desired
    docs_data = [
        {
            "name": "Auth",
            "endpoints": [
                {"method": "POST", "path": "/auth/login", "description": "User login"},
                {"method": "POST", "path": "/auth/register", "description": "User registration"}
            ]
        },
        {
            "name": "Books",
            "endpoints": [
                {"method": "GET", "path": "/books", "description": "List all books"},
                {"method": "POST", "path": "/books", "description": "Add a new book"},
                {"method": "GET", "path": "/books/<id>", "description": "Get details of a specific book"}
            ]
        },
        {
            "name": "Members",
            "endpoints": [
                {"method": "GET", "path": "/members", "description": "List members"},
                {"method": "PUT", "path": "/members/<id>", "description": "Update member info"}
            ]
        }
        # Add more sections for other blueprints as needed
    ]

    return render_template("docs/index.html", sections=docs_data)
