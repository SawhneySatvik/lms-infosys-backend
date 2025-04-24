-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. LIBRARIES Table
CREATE TABLE libraries (
    library_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    address TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    pincode INT8,
    admin_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 2. USERS Table
CREATE TABLE users (
    user_id UUID PRIMARY KEY, -- References auth.users.id
    library_id UUID NOT NULL REFERENCES libraries(library_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT CHECK (role IN ('Admin', 'Librarian', 'Member')) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    borrowed_book_ids UUID[] DEFAULT '{}',
    reserved_book_ids UUID[] DEFAULT '{}',
    wishlist_book_ids UUID[] DEFAULT '{}',
    user_image TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 3. GENRES Table
CREATE TABLE genres (
    genre_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 4. AUTHORS Table
CREATE TABLE authors (
    author_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    author_image TEXT,
    bio TEXT,
    book_ids UUID[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 5. BOOKS Table
CREATE TABLE books (
    book_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    library_id UUID NOT NULL REFERENCES libraries(library_id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    isbn TEXT UNIQUE,
    description TEXT,
    publisher_name TEXT,
    book_image TEXT,
    total_copies INT DEFAULT 1 CHECK (total_copies >= 0),
    available_copies INT DEFAULT 1 CHECK (available_copies >= 0),
    reserved_copies INT DEFAULT 0 CHECK (reserved_copies >= 0),
    author_ids UUID[] DEFAULT '{}',
    genre_ids UUID[] DEFAULT '{}',
    published_date TIMESTAMPTZ,
    added_on TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 6. POLICIES Table
CREATE TABLE policies (
    policy_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    library_id UUID NOT NULL REFERENCES libraries(library_id) ON DELETE CASCADE,
    max_borrow_days INT NOT NULL CHECK (max_borrow_days > 0),
    fine_per_day NUMERIC(6,2) NOT NULL CHECK (fine_per_day >= 0),
    max_books_per_user INT NOT NULL CHECK (max_books_per_user > 0),
    reservation_expiry_days INT NOT NULL CHECK (reservation_expiry_days > 0),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 7. BORROW_TRANSACTIONS Table
CREATE TABLE borrow_transactions (
    borrow_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    book_id UUID NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    borrow_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMPTZ,
    status TEXT CHECK (status IN ('borrowed', 'returned', 'overdue')) DEFAULT 'borrowed'
);

-- 8. RESERVATIONS Table
CREATE TABLE reservations (
    reservation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    book_id UUID NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    reserved_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ
);

-- 9. WISHLISTS Table
CREATE TABLE wishlists (
    wishlist_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    book_id UUID NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    added_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, book_id)
);

-- 10. REVIEWS Table
CREATE TABLE reviews (
    review_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    book_id UUID NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    reviewed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 11. TICKETS Table
CREATE TABLE tickets (
    ticket_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    resolved_by UUID REFERENCES users(user_id),
    type TEXT NOT NULL,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT CHECK (status IN ('open', 'in_progress', 'resolved')) DEFAULT 'open',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 12. FINES Table
CREATE TABLE fines (
    fine_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    borrow_id UUID NOT NULL REFERENCES borrow_transactions(borrow_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    book_id UUID NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    library_id UUID NOT NULL REFERENCES libraries(library_id) ON DELETE CASCADE,
    amount NUMERIC(8,2) NOT NULL CHECK (amount >= 0),
    reason TEXT,
    is_paid BOOLEAN DEFAULT FALSE,
    fine_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 13. DOCUMENT_UPLOADS Table
CREATE TABLE document_uploads (
    upload_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    book_id UUID REFERENCES books(book_id) ON DELETE SET NULL,
    library_id UUID NOT NULL REFERENCES libraries(library_id) ON DELETE CASCADE,
    file_url TEXT NOT NULL,
    file_type TEXT,
    uploaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- OTP Verification table
CREATE TABLE otp_verifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    otp TEXT NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);