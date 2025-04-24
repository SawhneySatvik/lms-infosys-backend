-- Trigger function for updating updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for updated_at
CREATE TRIGGER update_libraries_updated_at
BEFORE UPDATE ON libraries
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for updated_at
CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for updated_at
CREATE TRIGGER update_genres_updated_at
BEFORE UPDATE ON genres
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for updated_at
CREATE TRIGGER update_authors_updated_at
BEFORE UPDATE ON authors
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for updated_at
CREATE TRIGGER update_books_updated_at
BEFORE UPDATE ON books
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for updated_at
CREATE TRIGGER update_policies_updated_at
BEFORE UPDATE ON policies
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for updated_at
CREATE TRIGGER update_tickets_updated_at
BEFORE UPDATE ON tickets
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for updated_at
CREATE TRIGGER update_fines_updated_at
BEFORE UPDATE ON fines
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for updated_at
CREATE TRIGGER update_document_uploads_updated_at
BEFORE UPDATE ON document_uploads
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();