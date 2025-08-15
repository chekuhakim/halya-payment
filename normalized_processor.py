#!/usr/bin/env python3
"""
Script to process Excel file into normalized tables: residents and payments
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re
from datetime import datetime

def clean_text(text):
    """Clean text data"""
    if pd.isna(text):
        return None
    return str(text).strip()

def extract_numeric(value):
    """Extract numeric value from mixed data"""
    if pd.isna(value):
        return None
    try:
        return float(str(value))
    except:
        return None

def extract_integer(value):
    """Extract integer value from mixed data"""
    if pd.isna(value):
        return None
    try:
        return int(float(str(value)))
    except:
        return None

def create_resident_id(alley, house_number):
    """Create unique resident ID from alley and house number"""
    if pd.isna(alley) or pd.isna(house_number):
        return None
    return f"{alley}{house_number:03d}"  # e.g., "A001", "B023"

def process_fee_halya_sheet(df, sheet_name):
    """Process the Fee Halya 1 sheet into normalized structure"""
    
    # Data starts at row 7 (index 6)
    data_df = df.iloc[6:].copy()
    
    residents = []
    payments = []
    
    for idx, row in data_df.iterrows():
        # Skip empty rows
        if pd.isna(row.iloc[0]) and pd.isna(row.iloc[1]):
            continue
            
        # Extract resident data
        alley = clean_text(row.iloc[0])
        house_number = extract_integer(row.iloc[1])
        resident_name = clean_text(row.iloc[2])
        
        # Skip if no house number or name
        if pd.isna(house_number) or pd.isna(resident_name):
            continue
            
        # Create unique resident ID
        resident_id = create_resident_id(alley, house_number)
        if not resident_id:
            continue
            
        # Add resident record
        resident_record = {
            'resident_id': resident_id,
            'alley': alley,
            'house_number': house_number,
            'resident_name': resident_name,
            'sheet_name': sheet_name
        }
        residents.append(resident_record)
        
        # Extract and add payment records
        payments.extend(extract_payments(row, resident_id, sheet_name))
    
    return pd.DataFrame(residents), pd.DataFrame(payments)

def process_sticker_sheet(df, sheet_name):
    """Process the Sticker sheet into normalized structure"""
    
    # Data starts at row 7 (index 6)
    data_df = df.iloc[6:].copy()
    
    residents = []
    payments = []
    
    for idx, row in data_df.iterrows():
        # Skip empty rows
        if pd.isna(row.iloc[0]) and pd.isna(row.iloc[1]):
            continue
            
        # Extract resident data
        alley = clean_text(row.iloc[0])
        house_number = extract_integer(row.iloc[1])
        resident_name = clean_text(row.iloc[2])
        
        # Skip if no house number or name
        if pd.isna(house_number) or pd.isna(resident_name):
            continue
            
        # Create unique resident ID
        resident_id = create_resident_id(alley, house_number)
        if not resident_id:
            continue
            
        # Add resident record
        resident_record = {
            'resident_id': resident_id,
            'alley': alley,
            'house_number': house_number,
            'resident_name': resident_name,
            'sheet_name': sheet_name
        }
        residents.append(resident_record)
        
        # Extract and add payment records
        payments.extend(extract_payments(row, resident_id, sheet_name))
    
    return pd.DataFrame(residents), pd.DataFrame(payments)

def extract_payments(row, resident_id, sheet_name):
    """Extract all payment records from a resident row"""
    payments = []
    
    # Membership fee
    membership_fee = extract_numeric(row.iloc[4])
    if membership_fee and membership_fee > 0:
        membership_year = extract_integer(row.iloc[3])
        payments.append({
            'resident_id': resident_id,
            'payment_date': None,  # No specific date in Excel
            'description': 'Membership Fee',
            'amount': membership_fee,
            'year': membership_year,
            'sheet_name': sheet_name
        })
    
    # Annual fees by year
    annual_fee_2023 = extract_numeric(row.iloc[5])
    if annual_fee_2023 and annual_fee_2023 > 0:
        payments.append({
            'resident_id': resident_id,
            'payment_date': None,
            'description': 'Annual Fee 2023',
            'amount': annual_fee_2023,
            'year': 2023,
            'sheet_name': sheet_name
        })
    
    annual_fee_2024 = extract_numeric(row.iloc[6])
    if annual_fee_2024 and annual_fee_2024 > 0:
        payments.append({
            'resident_id': resident_id,
            'payment_date': None,
            'description': 'Annual Fee 2024',
            'amount': annual_fee_2024,
            'year': 2024,
            'sheet_name': sheet_name
        })
    
    annual_fee_2025 = extract_numeric(row.iloc[7])
    if annual_fee_2025 and annual_fee_2025 > 0:
        payments.append({
            'resident_id': resident_id,
            'payment_date': None,
            'description': 'Annual Fee 2025',
            'amount': annual_fee_2025,
            'year': 2025,
            'sheet_name': sheet_name
        })
    
    # Guard fees by month
    guard_fee_raya = extract_numeric(row.iloc[8])
    if guard_fee_raya and guard_fee_raya > 0:
        payments.append({
            'resident_id': resident_id,
            'payment_date': None,
            'description': 'Guard Fee - Raya',
            'amount': guard_fee_raya,
            'year': 2025,
            'sheet_name': sheet_name
        })
    
    guard_fee_april = extract_numeric(row.iloc[9])
    if guard_fee_april and guard_fee_april > 0:
        payments.append({
            'resident_id': resident_id,
            'payment_date': None,
            'description': 'Guard Fee - April 2025',
            'amount': guard_fee_april,
            'year': 2025,
            'sheet_name': sheet_name
        })
    
    # Additional guard fees (only in Fee Halya 1 sheet)
    if sheet_name == 'Fee Halya 1':
        guard_fee_may = extract_numeric(row.iloc[10])
        if guard_fee_may and guard_fee_may > 0:
            payments.append({
                'resident_id': resident_id,
                'payment_date': None,
                'description': 'Guard Fee - May 2025',
                'amount': guard_fee_may,
                'year': 2025,
                'sheet_name': sheet_name
            })
        
        guard_fee_june = extract_numeric(row.iloc[11])
        if guard_fee_june and guard_fee_june > 0:
            payments.append({
                'resident_id': resident_id,
                'payment_date': None,
                'description': 'Guard Fee - June 2025',
                'amount': guard_fee_june,
                'year': 2025,
                'sheet_name': sheet_name
            })
        
        guard_fee_july = extract_numeric(row.iloc[12])
        if guard_fee_july and guard_fee_july > 0:
            payments.append({
                'resident_id': resident_id,
                'payment_date': None,
                'description': 'Guard Fee - July 2025',
                'amount': guard_fee_july,
                'year': 2025,
                'sheet_name': sheet_name
            })
        
        guard_fee_august = extract_numeric(row.iloc[13])
        if guard_fee_august and guard_fee_august > 0:
            payments.append({
                'resident_id': resident_id,
                'payment_date': None,
                'description': 'Guard Fee - August 2025',
                'amount': guard_fee_august,
                'year': 2025,
                'sheet_name': sheet_name
            })
        
        # Excess payment
        excess_payment = extract_numeric(row.iloc[14])
        if excess_payment and excess_payment > 0:
            payments.append({
                'resident_id': resident_id,
                'payment_date': None,
                'description': 'Excess Payment Brought Forward',
                'amount': excess_payment,
                'year': 2025,
                'sheet_name': sheet_name
            })
    
    return payments

def process_excel_file(file_path):
    """Process Excel file and extract normalized data"""
    
    excel_file = pd.ExcelFile(file_path)
    all_residents = []
    all_payments = []
    
    print(f"Processing Excel file: {file_path}")
    print(f"Available sheets: {excel_file.sheet_names}")
    
    for sheet_name in excel_file.sheet_names:
        print(f"\nProcessing sheet: {sheet_name}")
        
        # Read the sheet
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        
        # Process based on sheet name
        if sheet_name == 'Fee Halya 1':
            residents, payments = process_fee_halya_sheet(df, sheet_name)
        elif sheet_name == 'Sticker':
            residents, payments = process_sticker_sheet(df, sheet_name)
        else:
            print(f"  Unknown sheet type: {sheet_name}")
            continue
        
        if len(residents) > 0:
            all_residents.append(residents)
            all_payments.append(payments)
            print(f"  Extracted {len(residents)} resident records")
            print(f"  Extracted {len(payments)} payment records")
        else:
            print(f"  No valid data found in {sheet_name}")
    
    # Combine all data
    if all_residents and all_payments:
        combined_residents = pd.concat(all_residents, ignore_index=True)
        combined_payments = pd.concat(all_payments, ignore_index=True)
        
        # Remove duplicates based on resident_id (in case same resident appears in both sheets)
        combined_residents = combined_residents.drop_duplicates(subset=['resident_id'], keep='first')
        
        # Clean up data types for CSV export
        combined_residents['house_number'] = combined_residents['house_number'].astype('Int64')  # nullable integer
        combined_payments['year'] = combined_payments['year'].astype('Int64')  # nullable integer
        
        return combined_residents, combined_payments
    else:
        return None, None

def generate_normalized_schema():
    """Generate normalized SQL schema with alley+house_number as unique ID"""
    
    schema = """
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
"""
    
    return schema

def main():
    excel_file = "Halya 1_Collection For Hiring Security Guards.xlsx"
    
    if not Path(excel_file).exists():
        print(f"Error: {excel_file} not found!")
        return
    
    # Process the Excel file
    residents_df, payments_df = process_excel_file(excel_file)
    
    if residents_df is None or payments_df is None:
        print("No data could be extracted from the Excel file.")
        return
    
    # Display sample of processed data
    print("\n" + "="*80)
    print("NORMALIZED DATA SAMPLE")
    print("="*80)
    
    print("\nRESIDENTS TABLE:")
    print(residents_df.head(10).to_string())
    print(f"\nTotal residents: {len(residents_df)}")
    
    print("\nPAYMENTS TABLE:")
    print(payments_df.head(10).to_string())
    print(f"\nTotal payments: {len(payments_df)}")
    
    # Show summary statistics
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    print(f"Total residents: {len(residents_df)}")
    print(f"Total payments: {len(payments_df)}")
    print(f"Total amount collected: RM {payments_df['amount'].sum():,.2f}")
    print(f"Average payment amount: RM {payments_df['amount'].mean():,.2f}")
    print(f"Residents with payments: {payments_df['resident_id'].nunique()}")
    
    # Payment types breakdown
    print(f"\nPayment types:")
    payment_types = payments_df.groupby('description')['amount'].agg(['count', 'sum']).round(2)
    for desc, row in payment_types.iterrows():
        print(f"  {desc}: {row['count']} payments, RM {row['sum']:,.2f}")
    
    # Save to CSV files with proper data types
    residents_csv = "residents_unique_id.csv"
    payments_csv = "payments_unique_id.csv"
    
    # Export with proper data types
    residents_df.to_csv(residents_csv, index=False, na_rep='')
    payments_df.to_csv(payments_csv, index=False, na_rep='')
    
    print(f"\nUnique ID data saved to:")
    print(f"  - {residents_csv} (Residents table)")
    print(f"  - {payments_csv} (Payments table)")
    
    # Generate normalized schema
    schema = generate_normalized_schema()
    
    with open('normalized_schema.sql', 'w') as f:
        f.write(schema)
    
    print("Normalized schema saved to: normalized_schema.sql")
    
    # Create summary report
    summary = f"""
NORMALIZED DATA PROCESSING SUMMARY
==================================

Source File: {excel_file}
Total Residents: {len(residents_df)}
Total Payments: {len(payments_df)}

Financial Summary:
- Total Amount Collected: RM {payments_df['amount'].sum():,.2f}
- Average Payment Amount: RM {payments_df['amount'].mean():,.2f}
- Residents with Payments: {payments_df['resident_id'].nunique()}

Payment Types:
"""
    
    for desc, row in payment_types.iterrows():
        summary += f"- {desc}: {row['count']} payments, RM {row['sum']:,.2f}\n"
    
    with open('normalized_summary.txt', 'w') as f:
        f.write(summary)
    
    print("\nNormalized summary saved to: normalized_summary.txt")
    print("\n" + "="*80)
    print("NORMALIZED PROCESSING COMPLETE")
    print("="*80)
    print("Files generated:")
    print(f"  - {residents_csv} (Residents table for Supabase)")
    print(f"  - {payments_csv} (Payments table for Supabase)")
    print("  - normalized_schema.sql (Normalized database schema)")
    print("  - normalized_summary.txt (Processing report)")

if __name__ == "__main__":
    main()
