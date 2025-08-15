-- Import Invoices into Halya Payment System
-- This script imports the generated invoices from CSV into the invoices table

-- First, let's create a temporary table to import the CSV data
CREATE TEMP TABLE temp_invoices (
    invoice_id INTEGER,
    resident_id VARCHAR(10),
    invoice_number VARCHAR(50),
    invoice_date DATE,
    due_date DATE,
    description VARCHAR(255),
    amount DECIMAL(10,2),
    status VARCHAR(20),
    payment_id INTEGER,
    year INTEGER,
    month INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Import the CSV data (you'll need to adjust the path based on your setup)
-- For Supabase, you can use the COPY command or import via the dashboard
-- This is a sample of the data structure

-- Insert sample invoices for demonstration
-- In production, you would use COPY command or Supabase dashboard import

INSERT INTO invoices (
    resident_id,
    invoice_number,
    invoice_date,
    due_date,
    description,
    amount,
    status,
    payment_id,
    year,
    month,
    created_at,
    updated_at
) VALUES 
-- Sample invoices for resident A001
('A001', 'INV-2025-000001', '2025-04-01', '2025-04-30', 'Guard Fee - April 2025', 30.00, 'PAID', NULL, 2025, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A001', 'INV-2025-000002', '2025-05-01', '2025-05-31', 'Guard Fee - May 2025', 30.00, 'PAID', NULL, 2025, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A001', 'INV-2025-000003', '2025-06-01', '2025-06-30', 'Guard Fee - June 2025', 30.00, 'PAID', NULL, 2025, 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Sample invoices for resident A002
('A002', 'INV-2023-000004', '2023-01-01', '2023-01-31', 'Membership Fee', 10.00, 'PAID', NULL, 2023, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A002', 'INV-2023-000005', '2023-01-01', '2023-01-31', 'Annual Fee 2023', 50.00, 'PAID', NULL, 2023, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A002', 'INV-2024-000006', '2024-01-01', '2024-01-31', 'Annual Fee 2024', 50.00, 'PAID', NULL, 2024, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A002', 'INV-2025-000007', '2025-01-01', '2025-01-31', 'Guard Fee - Raya', 30.00, 'PENDING', NULL, 2025, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A002', 'INV-2025-000008', '2025-04-01', '2025-04-30', 'Guard Fee - April 2025', 30.00, 'PAID', NULL, 2025, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A002', 'INV-2025-000009', '2025-05-01', '2025-05-31', 'Guard Fee - May 2025', 30.00, 'PAID', NULL, 2025, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A002', 'INV-2025-000010', '2025-06-01', '2025-06-30', 'Guard Fee - June 2025', 30.00, 'PAID', NULL, 2025, 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A002', 'INV-2025-000011', '2025-07-01', '2025-07-31', 'Guard Fee - July 2025', 30.00, 'PAID', NULL, 2025, 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A002', 'INV-2025-000012', '2025-08-01', '2025-08-31', 'Guard Fee - August 2025', 55.00, 'PENDING', NULL, 2025, 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A002', 'INV-2025-000013', '2025-01-01', '2025-01-31', 'Excess Payment Brought Forward', 110.00, 'PENDING', NULL, 2025, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Sample invoices for resident A003
('A003', 'INV-2023-000014', '2023-01-01', '2023-01-31', 'Membership Fee', 10.00, 'PAID', NULL, 2023, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A003', 'INV-2023-000015', '2023-01-01', '2023-01-31', 'Annual Fee 2023', 50.00, 'PAID', NULL, 2023, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A003', 'INV-2024-000016', '2024-01-01', '2024-01-31', 'Annual Fee 2024', 50.00, 'PAID', NULL, 2024, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A003', 'INV-2025-000017', '2025-01-01', '2025-01-31', 'Guard Fee - Raya', 30.00, 'PENDING', NULL, 2025, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A003', 'INV-2025-000018', '2025-04-01', '2025-04-30', 'Guard Fee - April 2025', 30.00, 'PAID', NULL, 2025, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A003', 'INV-2025-000019', '2025-05-01', '2025-05-31', 'Guard Fee - May 2025', 30.00, 'PAID', NULL, 2025, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A003', 'INV-2025-000020', '2025-06-01', '2025-06-30', 'Guard Fee - June 2025', 30.00, 'PAID', NULL, 2025, 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A003', 'INV-2025-000021', '2025-07-01', '2025-07-31', 'Guard Fee - July 2025', 30.00, 'PAID', NULL, 2025, 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('A003', 'INV-2025-000022', '2025-08-01', '2025-08-31', 'Guard Fee - August 2025', 55.00, 'PENDING', NULL, 2025, 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Verify the import
SELECT 
    COUNT(*) as total_invoices,
    COUNT(CASE WHEN status = 'PAID' THEN 1 END) as paid_invoices,
    COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as pending_invoices,
    COUNT(CASE WHEN status = 'OVERDUE' THEN 1 END) as overdue_invoices
FROM invoices;

-- Show sample data
SELECT 
    i.invoice_id,
    i.resident_id,
    r.resident_name,
    i.invoice_number,
    i.invoice_date,
    i.due_date,
    i.description,
    i.amount,
    i.status,
    i.year,
    i.month
FROM invoices i
JOIN residents r ON i.resident_id = r.resident_id
ORDER BY i.invoice_id
LIMIT 20;
