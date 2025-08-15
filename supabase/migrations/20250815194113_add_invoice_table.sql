-- Add Invoice Table and Related Components
-- This migration adds comprehensive invoice functionality to the Halya Payment System

-- Invoices table
CREATE TABLE invoices (
    invoice_id SERIAL PRIMARY KEY,
    resident_id VARCHAR(10) REFERENCES residents(resident_id) ON DELETE CASCADE,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    description VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'PAID', 'OVERDUE', 'CANCELLED')),
    payment_id INTEGER REFERENCES payments(id) ON DELETE SET NULL,
    year INTEGER,
    month INTEGER CHECK (month >= 1 AND month <= 12),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for invoice table performance
CREATE INDEX idx_invoices_resident_id ON invoices(resident_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_date ON invoices(invoice_date);
CREATE INDEX idx_invoices_due_date ON invoices(due_date);
CREATE INDEX idx_invoices_year_month ON invoices(year, month);
CREATE INDEX idx_invoices_payment_id ON invoices(payment_id);

-- View for invoice summary
CREATE VIEW invoice_summary AS
SELECT 
    r.resident_id,
    r.alley,
    r.house_number,
    r.resident_name,
    COUNT(i.invoice_id) as total_invoices,
    SUM(CASE WHEN i.status = 'PAID' THEN i.amount ELSE 0 END) as paid_amount,
    SUM(CASE WHEN i.status = 'PENDING' THEN i.amount ELSE 0 END) as pending_amount,
    SUM(CASE WHEN i.status = 'OVERDUE' THEN i.amount ELSE 0 END) as overdue_amount,
    COUNT(CASE WHEN i.status = 'PAID' THEN 1 END) as paid_count,
    COUNT(CASE WHEN i.status = 'PENDING' THEN 1 END) as pending_count,
    COUNT(CASE WHEN i.status = 'OVERDUE' THEN 1 END) as overdue_count
FROM residents r
LEFT JOIN invoices i ON r.resident_id = i.resident_id
GROUP BY r.resident_id, r.alley, r.house_number, r.resident_name;

-- Function to generate invoice number
CREATE OR REPLACE FUNCTION generate_invoice_number()
RETURNS VARCHAR(50) AS $$
DECLARE
    next_number INTEGER;
    invoice_num VARCHAR(50);
BEGIN
    SELECT COALESCE(MAX(CAST(SUBSTRING(invoice_number FROM 9) AS INTEGER)), 0) + 1
    INTO next_number
    FROM invoices
    WHERE invoice_number LIKE 'INV-' || EXTRACT(YEAR FROM CURRENT_DATE) || '-%';
    
    invoice_num := 'INV-' || EXTRACT(YEAR FROM CURRENT_DATE) || '-' || LPAD(next_number::TEXT, 6, '0');
    RETURN invoice_num;
END;
$$ LANGUAGE plpgsql;

-- Function to update invoice status based on due date
CREATE OR REPLACE FUNCTION update_invoice_status()
RETURNS TRIGGER AS $$
BEGIN
    -- Update status to OVERDUE if due date has passed and status is still PENDING
    IF NEW.due_date < CURRENT_DATE AND NEW.status = 'PENDING' THEN
        NEW.status := 'OVERDUE';
    END IF;
    
    -- Update status to PAID if payment_id is set
    IF NEW.payment_id IS NOT NULL AND NEW.status != 'PAID' THEN
        NEW.status := 'PAID';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update invoice updated_at timestamp
CREATE TRIGGER update_invoices_updated_at 
    BEFORE UPDATE ON invoices 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger to automatically update invoice status
CREATE TRIGGER update_invoice_status_trigger
    BEFORE INSERT OR UPDATE ON invoices
    FOR EACH ROW
    EXECUTE FUNCTION update_invoice_status();
