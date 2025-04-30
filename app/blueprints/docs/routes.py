from flask import render_template
from . import docs_bp

@docs_bp.route('/')
def index():
    docs_data = [
        {
            "name": "Auth",
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/auth/admin/register",
                    "description": "Register an admin and create a library",
                    "headers": [{"key": "Content-Type", "value": "multipart/form-data"}],
                    "request_body": {
                        "email": "admin@example.com",
                        "password": "Admin1234",
                        "name": "Admin User",
                        "library_name": "City Library",
                        "address": "123 Main St",
                        "city": "Springfield",
                        "state": "IL",
                        "country": "USA",
                        "pincode": "62701"
                    },
                    "response_body": {
                        "message": "Admin registered successfully. You can now sign in.",
                        "user_id": "<uuid>",
                        "library_id": "<uuid>"
                    },
                    "status_code": 201
                },
                {
                    "method": "POST",
                    "path": "/auth/signin",
                    "description": "Sign in a user (Admin, Librarian, or Member)",
                    "headers": [{"key": "Content-Type", "value": "application/json"}],
                    "request_body": {
                        "email": "user@example.com",
                        "password": "Password1234"
                    },
                    "response_body": {
                        "message": "Please verify OTP sent to your email to complete login.",
                        "user_id": "<uuid>"
                    },
                    "status_code": 200
                },
                {
                    "method": "POST",
                    "path": "/auth/verify-otp",
                    "description": "Verify OTP for signup or signin",
                    "headers": [{"key": "Content-Type", "value": "application/json"}],
                    "request_body": {
                        "user_id": "<uuid>",
                        "otp": "123456"
                    },
                    "response_body": {
                        "message": "OTP verified successfully. Signed in successfully.",
                        "access_token": "<token>",
                        "refresh_token": "<token>",
                        "user": {
                            "user_id": "<uuid>",
                            "name": "User Name",
                            "email": "user@example.com",
                            "role": "Role",
                            "user_image": "null"
                        }
                    },
                    "status_code": 200
                },
                {
                    "method": "POST",
                    "path": "/auth/librarian/register",
                    "description": "Register a librarian (admin only)",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <admin_token>"},
                        {"key": "Content-Type", "value": "multipart/form-data"}
                    ],
                    "request_body": {
                        "email": "librarian@example.com",
                        "name": "Librarian User"
                    },
                    "response_body": {
                        "message": "Librarian registered successfully. Credentials have been sent to their email.",
                        "user_id": "<uuid>"
                    },
                    "status_code": 201
                },
                {
                    "method": "POST",
                    "path": "/auth/signup",
                    "description": "Register a member",
                    "headers": [{"key": "Content-Type", "value": "multipart/form-data"}],
                    "request_body": {
                        "email": "member@example.com",
                        "password": "Member1234",
                        "name": "Member User",
                        "library_id": "<library_uuid>",
                        "preferred_genre_ids": ["<genre_uuid>"]
                    },
                    "response_body": {
                        "message": "User registered successfully. Please verify OTP sent to your email.",
                        "user_id": "<uuid>"
                    },
                    "status_code": 201
                },
                {
                    "method": "POST",
                    "path": "/auth/refresh",
                    "description": "Refresh access token",
                    "headers": [{"key": "Content-Type", "value": "application/json"}],
                    "request_body": {
                        "refresh_token": "<refresh_token>"
                    },
                    "response_body": {
                        "message": "Token refreshed successfully",
                        "access_token": "<new_token>",
                        "refresh_token": "<new_token>",
                        "user": {
                            "user_id": "<uuid>",
                            "name": "User Name",
                            "email": "user@example.com",
                            "role": "Role",
                            "user_image": "null"
                        }
                    },
                    "status_code": 200
                },
                {
                    "method": "POST",
                    "path": "/auth/signout",
                    "description": "Sign out a user",
                    "headers": [{"key": "Authorization", "value": "Bearer <token>"}],
                    "request_body": {},
                    "response_body": {
                        "message": "Logged out successfully"
                    },
                    "status_code": 200
                },
                {
                    "method": "GET",
                    "path": "/auth/profile",
                    "description": "Get user profile",
                    "headers": [{"key": "Authorization", "value": "Bearer <token>"}],
                    "request_body": {},
                    "response_body": {
                        "user": {
                            "user_id": "<uuid>",
                            "name": "User Name",
                            "email": "user@example.com",
                            "role": "Role",
                            "library_id": "<uuid>",
                            "user_image": "null",
                            "preferred_genre_ids": []
                        }
                    },
                    "status_code": 200
                },
                {
                    "method": "PATCH",
                    "path": "/auth/profile",
                    "description": "Update user profile",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <token>"},
                        {"key": "Content-Type", "value": "multipart/form-data"}
                    ],
                    "request_body": {
                        "name": "Updated Name",
                        "preferred_genre_ids": ["<genre_uuid>"]
                    },
                    "response_body": {
                        "message": "Profile updated successfully",
                        "user": {
                            "user_id": "<uuid>",
                            "name": "Updated Name",
                            "email": "user@example.com",
                            "role": "Role",
                            "user_image": "null",
                            "preferred_genre_ids": ["<genre_uuid>"]
                        }
                    },
                    "status_code": 200
                },
                {
                    "method": "POST",
                    "path": "/auth/reset-password",
                    "description": "Request password reset",
                    "headers": [{"key": "Content-Type", "value": "application/json"}],
                    "request_body": {
                        "email": "user@example.com"
                    },
                    "response_body": {
                        "message": "Password reset email sent"
                    },
                    "status_code": 200
                }
            ]
        },
        {
            "name": "Admin",
            "endpoints": [
                {
                    "method": "GET",
                    "path": "/admin/dashboard",
                    "description": "Get admin dashboard metrics",
                    "headers": [{"key": "Authorization", "value": "Bearer <admin_token>"}],
                    "request_body": {},
                    "response_body": {
                        "total_books": 10,
                        "total_members": 5,
                        "total_librarians": 2,
                        "active_borrowings": 3,
                        "outstanding_fines": 50.00
                    },
                    "status_code": 200
                },
                {
                    "method": "GET",
                    "path": "/admin/settings",
                    "description": "Get library settings",
                    "headers": [{"key": "Authorization", "value": "Bearer <admin_token>"}],
                    "request_body": {},
                    "response_body": {
                        "fine_rate": 1.50,
                        "max_borrow_days": 14
                    },
                    "status_code": 200
                },
                {
                    "method": "PATCH",
                    "path": "/admin/settings",
                    "description": "Update library settings",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <admin_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "fine_rate": 2.00,
                        "max_borrow_days": 21
                    },
                    "response_body": {
                        "message": "Settings updated successfully"
                    },
                    "status_code": 200
                },
                {
                    "method": "GET",
                    "path": "/admin/reports",
                    "description": "Get library reports",
                    "headers": [{"key": "Authorization", "value": "Bearer <admin_token>"}],
                    "request_body": {},
                    "response_body": {
                        "report": "<report_data>"
                    },
                    "status_code": 200
                },
                {
                    "method": "GET",
                    "path": "/admin/users",
                    "description": "List all users",
                    "headers": [{"key": "Authorization", "value": "Bearer <admin_token>"}],
                    "request_body": {},
                    "response_body": {
                        "users": [
                            {
                                "user_id": "<uuid>",
                                "name": "Member One",
                                "email": "member1@example.com",
                                "is_active": "true"
                            }
                        ],
                        "total": 1,
                        "pages": 1,
                        "page": 1
                    },
                    "status_code": 200
                },
                {
                    "method": "PATCH",
                    "path": "/admin/users/<user_id>",
                    "description": "Update user details",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <admin_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "is_active": "false"
                    },
                    "response_body": {
                        "message": "User updated successfully"
                    },
                    "status_code": 200
                }
            ]
        },
        {
            "name": "Librarians",
            "endpoints": [
                {
                    "method": "GET",
                    "path": "/librarians",
                    "description": "List all librarians",
                    "headers": [{"key": "Authorization", "value": "Bearer <admin_token>"}],
                    "request_body": {},
                    "response_body": {
                        "librarians": [
                            {
                                "user_id": "<uuid>",
                                "name": "Librarian One",
                                "email": "librarian1@example.com",
                                "is_active": "true"
                            }
                        ],
                        "total": 1,
                        "pages": 1,
                        "page": 1
                    },
                    "status_code": 200
                },
                {
                    "method": "GET",
                    "path": "/librarians/<librarian_id>",
                    "description": "Get librarian details",
                    "headers": [{"key": "Authorization", "value": "Bearer <admin_token>"}],
                    "request_body": {},
                    "response_body": {
                        "user_id": "<uuid>",
                        "name": "Librarian One",
                        "email": "librarian1@example.com",
                        "is_active": "true"
                    },
                    "status_code": 200
                },
                {
                    "method": "PATCH",
                    "path": "/librarians/<librarian_id>",
                    "description": "Update librarian details",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <admin_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "name": "Updated Librarian",
                        "is_active": "false"
                    },
                    "response_body": {
                        "message": "Librarian updated successfully"
                    },
                    "status_code": 200
                },
                {
                    "method": "DELETE",
                    "path": "/librarians/<librarian_id>",
                    "description": "Delete a librarian",
                    "headers": [{"key": "Authorization", "value": "Bearer <admin_token>"}],
                    "request_body": {},
                    "response_body": {
                        "message": "Librarian deleted successfully"
                    },
                    "status_code": 200
                }
            ]
        },
        {
            "name": "Members",
            "endpoints": [
                {
                    "method": "GET",
                    "path": "/members",
                    "description": "List all members",
                    "headers": [{"key": "Authorization", "value": "Bearer <admin_token_or_librarian_token>"}],
                    "request_body": {},
                    "response_body": {
                        "members": [
                            {
                                "user_id": "<uuid>",
                                "name": "Member One",
                                "email": "member1@example.com",
                                "is_active": "true"
                            }
                        ],
                        "total": 1,
                        "pages": 1,
                        "page": 1
                    },
                    "status_code": 200
                },
                {
                    "method": "GET",
                    "path": "/members/<member_id>",
                    "description": "Get member details",
                    "headers": [{"key": "Authorization", "value": "Bearer <admin_token_or_librarian_token>"}],
                    "request_body": {},
                    "response_body": {
                        "user_id": "<uuid>",
                        "name": "Member One",
                        "email": "member1@example.com",
                        "is_active": "true"
                    },
                    "status_code": 200
                },
                {
                    "method": "PATCH",
                    "path": "/members/<member_id>",
                    "description": "Update member details",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <admin_token_or_librarian_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "name": "Updated Member",
                        "is_active": "false"
                    },
                    "response_body": {
                        "message": "Member updated successfully"
                    },
                    "status_code": 200
                },
                {
                    "method": "DELETE",
                    "path": "/members/<member_id>",
                    "description": "Delete a member",
                    "headers": [{"key": "Authorization", "value": "Bearer <admin_token_or_librarian_token>"}],
                    "request_body": {},
                    "response_body": {
                        "message": "Member deleted successfully"
                    },
                    "status_code": 200
                }
            ]
        },
        {
            "name": "Books",
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/books",
                    "description": "Add a new book",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <librarian_token>"},
                        {"key": "Content-Type", "value": "multipart/form-data"}
                    ],
                    "request_body": {
                        "title": "Sample Book",
                        "isbn": "1234567890123",
                        "description": "A sample book.",
                        "publisher_name": "Sample Publisher",
                        "total_copies": 5,
                        "author_ids": "<author_uuid>",
                        "genre_ids": "<genre_uuid>",
                        "published_date": "2023-01-01"
                    },
                    "response_body": {
                        "message": "Book created successfully",
                        "book_id": "<uuid>"
                    },
                    "status_code": 201
                },
                {
                    "method": "GET",
                    "path": "/books",
                    "description": "List all books",
                    "headers": [{"key": "Authorization", "value": "Bearer <member_token>"}],
                    "request_body": {},
                    "response_body": {
                        "books": [
                            {
                                "book_id": "<uuid>",
                                "title": "Sample Book",
                                "isbn": "1234567890123",
                                "description": "A sample book.",
                                "publisher_name": "Sample Publisher",
                                "total_copies": 5,
                                "available_copies": 5
                            }
                        ],
                        "total": 1,
                        "pages": 1,
                        "page": 1
                    },
                    "status_code": 200
                },
                {
                    "method": "GET",
                    "path": "/books/<book_id>",
                    "description": "Get details of a specific book",
                    "headers": [{"key": "Authorization", "value": "Bearer <member_token>"}],
                    "request_body": {},
                    "response_body": {
                        "book": {
                            "book_id": "<uuid>",
                            "title": "Sample Book",
                            "isbn": "1234567890123",
                            "description": "A sample book.",
                            "publisher_name": "Sample Publisher",
                            "total_copies": 5,
                            "available_copies": 5
                        }
                    },
                    "status_code": 200
                },
                {
                    "method": "PATCH",
                    "path": "/books/<book_id>",
                    "description": "Update book details",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <librarian_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "title": "Updated Book Title"
                    },
                    "response_body": {
                        "message": "Book updated successfully",
                        "book_id": "<uuid>"
                    },
                    "status_code": 200
                },
                {
                    "method": "DELETE",
                    "path": "/books/<book_id>",
                    "description": "Delete a book",
                    "headers": [{"key": "Authorization", "value": "Bearer <librarian_token>"}],
                    "request_body": {},
                    "response_body": {
                        "message": "Book deleted successfully"
                    },
                    "status_code": 200
                }
            ]
        },
        {
            "name": "Authors",
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/authors",
                    "description": "Add a new author",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <librarian_token>"},
                        {"key": "Content-Type", "value": "multipart/form-data"}
                    ],
                    "request_body": {
                        "name": "Author Name",
                        "bio": "Author biography."
                    },
                    "response_body": {
                        "message": "Author created successfully",
                        "author_id": "<uuid>"
                    },
                    "status_code": 201
                },
                {
                    "method": "GET",
                    "path": "/authors",
                    "description": "List all authors",
                    "headers": [{"key": "Authorization", "value": "Bearer <member_token>"}],
                    "request_body": {},
                    "response_body": {
                        "authors": [
                            {
                                "author_id": "<uuid>",
                                "name": "Author Name",
                                "bio": "Author biography."
                            }
                        ],
                        "total": 1,
                        "pages": 1,
                        "page": 1
                    },
                    "status_code": 200
                },
                {
                    "method": "GET",
                    "path": "/authors/<author_id>",
                    "description": "Get author details",
                    "headers": [{"key": "Authorization", "value": "Bearer <member_token>"}],
                    "request_body": {},
                    "response_body": {
                        "author": {
                            "author_id": "<uuid>",
                            "name": "Author Name",
                            "bio": "Author biography."
                        }
                    },
                    "status_code": 200
                },
                {
                    "method": "PATCH",
                    "path": "/authors/<author_id>",
                    "description": "Update author details",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <librarian_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "name": "Updated Author Name"
                    },
                    "response_body": {
                        "message": "Author updated successfully",
                        "author_id": "<uuid>"
                    },
                    "status_code": 200
                },
                {
                    "method": "DELETE",
                    "path": "/authors/<author_id>",
                    "description": "Delete an author",
                    "headers": [{"key": "Authorization", "value": "Bearer <librarian_token>"}],
                    "request_body": {},
                    "response_body": {
                        "message": "Author deleted successfully"
                    },
                    "status_code": 200
                }
            ]
        },
        {
            "name": "Genres",
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/genres",
                    "description": "Add a new genre",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <librarian_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "name": "Fiction",
                        "description": "Books that are fictional."
                    },
                    "response_body": {
                        "message": "Genre created successfully",
                        "genre_id": "<uuid>"
                    },
                    "status_code": 201
                },
                {
                    "method": "GET",
                    "path": "/genres",
                    "description": "List all genres",
                    "headers": [{"key": "Authorization", "value": "Bearer <member_token>"}],
                    "request_body": {},
                    "response_body": {
                        "genres": [
                            {
                                "genre_id": "<uuid>",
                                "name": "Fiction",
                                "description": "Books that are fictional."
                            }
                        ],
                        "total": 1,
                        "pages": 1,
                        "page": 1
                    },
                    "status_code": 200
                },
                {
                    "method": "GET",
                    "path": "/genres/<genre_id>",
                    "description": "Get genre details",
                    "headers": [{"key": "Authorization", "value": "Bearer <member_token>"}],
                    "request_body": {},
                    "response_body": {
                        "genre": {
                            "genre_id": "<uuid>",
                            "name": "Fiction",
                            "description": "Books that are fictional."
                        }
                    },
                    "status_code": 200
                },
                {
                    "method": "PATCH",
                    "path": "/genres/<genre_id>",
                    "description": "Update genre details",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <librarian_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "name": "Updated Fiction"
                    },
                    "response_body": {
                        "message": "Genre updated successfully",
                        "genre_id": "<uuid>"
                    },
                    "status_code": 200
                },
                {
                    "method": "DELETE",
                    "path": "/genres/<genre_id>",
                    "description": "Delete a genre",
                    "headers": [{"key": "Authorization", "value": "Bearer <librarian_token>"}],
                    "request_body": {},
                    "response_body": {
                        "message": "Genre deleted successfully"
                    },
                    "status_code": 200
                }
            ]
        },
        {
            "name": "Wishlist",
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/wishlist",
                    "description": "Add a book to wishlist",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <member_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "book_id": "<book_uuid>"
                    },
                    "response_body": {
                        "message": "Book added to wishlist",
                        "wishlist_id": "<uuid>"
                    },
                    "status_code": 201
                },
                {
                    "method": "GET",
                    "path": "/wishlist",
                    "description": "List wishlist items",
                    "headers": [{"key": "Authorization", "value": "Bearer <member_token>"}],
                    "request_body": {},
                    "response_body": {
                        "wishlists": [
                            {
                                "wishlist_id": "<uuid>",
                                "book_id": "<book_uuid>",
                                "added_at": "<iso_date>"
                            }
                        ]
                    },
                    "status_code": 200
                },
                {
                    "method": "DELETE",
                    "path": "/wishlist/<wishlist_id>",
                    "description": "Remove a book from wishlist",
                    "headers": [{"key": "Authorization", "value": "Bearer <member_token>"}],
                    "request_body": {},
                    "response_body": {
                        "message": "Book removed from wishlist"
                    },
                    "status_code": 200
                }
            ]
        },
        {
            "name": "Reservations",
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/reservations",
                    "description": "Create a book reservation",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <member_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "book_id": "<book_uuid>"
                    },
                    "response_body": {
                        "message": "Reservation created",
                        "reservation_id": "<uuid>"
                    },
                    "status_code": 201
                },
                {
                    "method": "GET",
                    "path": "/reservations",
                    "description": "List all reservations",
                    "headers": [{"key": "Authorization", "value": "Bearer <librarian_token>"}],
                    "request_body": {},
                    "response_body": {
                        "reservations": [
                            {
                                "reservation_id": "<uuid>",
                                "book_id": "<book_uuid>",
                                "status": "pending",
                                "created_at": "<iso_date>"
                            }
                        ]
                    },
                    "status_code": 200
                },
                {
                    "method": "PATCH",
                    "path": "/reservations/<reservation_id>",
                    "description": "Update reservation status",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <librarian_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "status": "confirmed"
                    },
                    "response_body": {
                        "message": "Reservation updated"
                    },
                    "status_code": 200
                }
            ]
        },
        {
            "name": "Borrow",
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/borrow",
                    "description": "Borrow a book",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <librarian_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "reservation_id": "<reservation_uuid>"
                    },
                    "response_body": {
                        "message": "Book borrowed",
                        "borrow_id": "<uuid>"
                    },
                    "status_code": 201
                },
                {
                    "method": "PATCH",
                    "path": "/borrow/<borrow_id>",
                    "description": "Return a borrowed book",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <librarian_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "borrow_id": "<borrow_uuid>"
                    },
                    "response_body": {
                        "message": "Book returned"
                    },
                    "status_code": 200
                }
            ]
        },
        {
            "name": "Fines",
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/fines",
                    "description": "Create a fine",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <librarian_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "borrow_id": "<borrow_uuid>",
                        "amount": 10.00,
                        "reason": "Manual fine"
                    },
                    "response_body": {
                        "message": "Fine created",
                        "fine_id": "<uuid>"
                    },
                    "status_code": 201
                },
                {
                    "method": "GET",
                    "path": "/fines",
                    "description": "List fines for a user",
                    "headers": [{"key": "Authorization", "value": "Bearer <member_token>"}],
                    "request_body": {},
                    "response_body": {
                        "fines": [
                            {
                                "fine_id": "<uuid>",
                                "borrow_id": "<borrow_uuid>",
                                "amount": 10.00,
                                "reason": "Manual fine",
                                "is_paid": "false"
                            }
                        ]
                    },
                    "status_code": 200
                },
                {
                    "method": "PATCH",
                    "path": "/fines/<fine_id>",
                    "description": "Update fine status (e.g., mark as paid)",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <member_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "is_paid": "true"
                    },
                    "response_body": {
                        "message": "Fine updated"
                    },
                    "status_code": 200
                }
            ]
        },
        {
            "name": "Tickets",
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/tickets",
                    "description": "Create a support ticket",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <librarian_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "type": "request",
                        "subject": "Need more books",
                        "message": "Please add more fiction books.",
                        "priority": "high"
                    },
                    "response_body": {
                        "message": "Ticket created",
                        "ticket_id": "<uuid>"
                    },
                    "status_code": 201
                },
                {
                    "method": "GET",
                    "path": "/tickets",
                    "description": "List all tickets",
                    "headers": [{"key": "Authorization", "value": "Bearer <admin_token>"}],
                    "request_body": {},
                    "response_body": {
                        "tickets": [
                            {
                                "ticket_id": "<uuid>",
                                "type": "request",
                                "subject": "Need more books",
                                "status": "open",
                                "priority": "high"
                            }
                        ]
                    },
                    "status_code": 200
                },
                {
                    "method": "PATCH",
                    "path": "/tickets/<ticket_id>",
                    "description": "Update ticket status",
                    "headers": [
                        {"key": "Authorization", "value": "Bearer <admin_token>"},
                        {"key": "Content-Type", "value": "application/json"}
                    ],
                    "request_body": {
                        "status": "resolved"
                    },
                    "response_body": {
                        "message": "Ticket updated"
                    },
                    "status_code": 200
                }
            ]
        }
    ]

    return render_template("docs/index.html", sections=docs_data)