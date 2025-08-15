-- Normalized SQL Schema for Halya Security Guards Data
-- Generated from processed Excel data
-- Uses alley+house_number as unique resident identifier

-- Residents table
CREATE TABLE residents (
    resident_id VARCHAR(10) PRIMARY KEY,  -- e.g., "A001", "B023"
    alley VARCHAR(10) NOT NULL,
    house_number INTEGER NOT NULL,
    resident_name VARCHAR(255) NOT NULL,
    sheet_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(alley, house_number)  -- Ensure alley+house_number is unique
);

-- Payments table
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    resident_id VARCHAR(10) REFERENCES residents(resident_id) ON DELETE CASCADE,
    payment_date DATE,
    description VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    year INTEGER,
    sheet_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better query performance
CREATE INDEX idx_residents_house_number ON residents(house_number);
CREATE INDEX idx_residents_name ON residents(resident_name);
CREATE INDEX idx_residents_alley ON residents(alley);
CREATE INDEX idx_payments_resident_id ON payments(resident_id);
CREATE INDEX idx_payments_year ON payments(year);
CREATE INDEX idx_payments_description ON payments(description);

-- View for resident summary with total payments
CREATE VIEW resident_summary AS
SELECT 
    r.resident_id,
    r.alley,
    r.house_number,
    r.resident_name,
    r.sheet_name,
    COUNT(p.id) as total_payments,
    SUM(p.amount) as total_amount,
    AVG(p.amount) as avg_payment_amount
FROM residents r
LEFT JOIN payments p ON r.resident_id = p.resident_id
GROUP BY r.resident_id, r.alley, r.house_number, r.resident_name, r.sheet_name;

-- View for payment summary by type
CREATE VIEW payment_summary AS
SELECT 
    description,
    year,
    COUNT(*) as payment_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM payments
GROUP BY description, year
ORDER BY year DESC, total_amount DESC;

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers to automatically update updated_at
CREATE TRIGGER update_residents_updated_at 
    BEFORE UPDATE ON residents 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_payments_updated_at 
    BEFORE UPDATE ON payments 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
