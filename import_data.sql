-- Import script for Halya Payment Data
-- Run this in the Supabase SQL Editor

-- First, let's check if tables exist
SELECT 'residents' as table_name, COUNT(*) as row_count FROM residents
UNION ALL
SELECT 'payments' as table_name, COUNT(*) as row_count FROM payments;

-- IMPORT INSTRUCTIONS:
-- The CSV files now use meaningful unique IDs (alley+house_number format).
-- Use these files for import:
-- 1. residents_unique_id.csv (147 residents with unique IDs like "A001", "B023")
-- 2. payments_unique_id.csv (1,540 payments linked by resident_id)

-- To import via Supabase Dashboard:
-- 1. Go to your Supabase dashboard: https://supabase.com/dashboard/project/dxsjgwsaycdspfjasitz
-- 2. Navigate to Table Editor
-- 3. Click on "residents" table
-- 4. Click "Import data" and upload residents_unique_id.csv
-- 5. Repeat for "payments" table with payments_unique_id.csv

-- IMPORTANT: Import residents_unique_id.csv FIRST, then payments_unique_id.csv
-- This ensures the foreign key relationships work correctly.

-- Sample data for testing (if you want to test with a few records first):

-- Sample resident data (first 5 records with unique IDs)
INSERT INTO residents (resident_id, alley, house_number, resident_name, sheet_name) VALUES
('A001', 'A', 1, 'Ameer Shah', 'Fee Halya 1'),
('A002', 'A', 2, 'Logaruthran A/L Muniappan', 'Fee Halya 1'),
('A003', 'A', 3, 'Ramohan A/L Narasimma Roa', 'Fee Halya 1'),
('A004', 'A', 4, 'Muhamad Zaiful Azree Bin Khairi', 'Fee Halya 1'),
('A005', 'A', 5, 'Uma Rani A/P Rama Rao', 'Fee Halya 1')
ON CONFLICT (resident_id) DO NOTHING;

-- Sample payment data (first 10 records)
INSERT INTO payments (resident_id, payment_date, description, amount, year, sheet_name) VALUES
('A001', NULL, 'Guard Fee - April 2025', 30.00, 2025, 'Fee Halya 1'),
('A001', NULL, 'Guard Fee - May 2025', 30.00, 2025, 'Fee Halya 1'),
('A001', NULL, 'Guard Fee - June 2025', 30.00, 2025, 'Fee Halya 1'),
('A002', NULL, 'Membership Fee', 10.00, 2023, 'Fee Halya 1'),
('A002', NULL, 'Annual Fee 2023', 50.00, 2023, 'Fee Halya 1'),
('A002', NULL, 'Annual Fee 2024', 50.00, 2024, 'Fee Halya 1'),
('A002', NULL, 'Guard Fee - Raya', 30.00, 2025, 'Fee Halya 1'),
('A002', NULL, 'Guard Fee - April 2025', 30.00, 2025, 'Fee Halya 1'),
('A002', NULL, 'Guard Fee - May 2025', 30.00, 2025, 'Fee Halya 1'),
('A002', NULL, 'Guard Fee - June 2025', 30.00, 2025, 'Fee Halya 1')
ON CONFLICT (id) DO NOTHING;

-- Check the imported data
SELECT 'residents' as table_name, COUNT(*) as row_count FROM residents
UNION ALL
SELECT 'payments' as table_name, COUNT(*) as row_count FROM payments;

-- Test the views
SELECT * FROM resident_summary LIMIT 5;
SELECT * FROM payment_summary LIMIT 10;
