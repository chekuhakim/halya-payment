#!/usr/bin/env python3
"""
Generate invoices for all residents based on the 8 payment types from payments_rows-3.csv
This creates invoices for all residents so we can track who has paid and who hasn't
"""

import csv
import datetime
from typing import List, Dict

def parse_month_from_description(description: str) -> int:
    """Extract month number from description like 'Guard Fee - April 2025'"""
    month_mapping = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    
    description_lower = description.lower()
    for month_name, month_num in month_mapping.items():
        if month_name in description_lower:
            return month_num
    return None

def generate_invoice_date(year: int, month: int = None) -> datetime.date:
    """Generate invoice date based on year and month"""
    if month:
        # Use 1st of the month for guard fees
        return datetime.date(year, month, 1)
    else:
        # For annual/membership fees, use January 1st
        return datetime.date(year, 1, 1)

def generate_due_date(invoice_date: datetime.date, description: str) -> datetime.date:
    """Generate due date (30 days from invoice date for most fees)"""
    if 'guard fee' in description.lower():
        # Guard fees due by end of month
        if invoice_date.month == 12:
            return datetime.date(invoice_date.year + 1, 1, 31)
        else:
            return datetime.date(invoice_date.year, invoice_date.month + 1, 1) - datetime.timedelta(days=1)
    else:
        # Other fees due 30 days from invoice date
        return invoice_date + datetime.timedelta(days=30)

def generate_invoice_number(invoice_id: int, year: int) -> str:
    """Generate invoice number in format INV-YYYY-XXXXXX"""
    return f"INV-{year}-{invoice_id:06d}"

def generate_invoices_for_all_residents(payment_template_file: str, residents_file: str, output_file: str):
    """Generate invoices for all residents based on the 8 payment types"""
    
    # Read the 8 payment templates
    payment_templates = []
    with open(payment_template_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            payment_templates.append({
                'description': row['description'],
                'amount': float(row['amount']),
                'year': int(row['year'])
            })
    
    # Read all residents
    residents = []
    with open(residents_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            residents.append(row['resident_id'])
    
    print(f"Found {len(payment_templates)} payment templates")
    print(f"Found {len(residents)} residents")
    
    # Generate invoices
    invoices = []
    invoice_id = 1
    
    for resident_id in residents:
        for template in payment_templates:
            description = template['description']
            amount = template['amount']
            year = template['year']
            
            # Parse month from description
            month = parse_month_from_description(description)
            
            # Generate dates
            invoice_date = generate_invoice_date(year, month)
            due_date = generate_due_date(invoice_date, description)
            
            # All invoices start as PENDING (we'll track who actually paid)
            status = 'PENDING'
            
            # Generate invoice number
            invoice_number = generate_invoice_number(invoice_id, year)
            
            # Create invoice record
            invoice = {
                'invoice_id': invoice_id,
                'resident_id': resident_id,
                'invoice_number': invoice_number,
                'invoice_date': invoice_date.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'description': description,
                'amount': amount,
                'status': status,
                'payment_id': None,  # Will be linked when payment is made
                'year': year,
                'month': month if month else 1,
                'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            invoices.append(invoice)
            invoice_id += 1
    
    # Write to CSV
    fieldnames = [
        'invoice_id', 'resident_id', 'invoice_number', 'invoice_date', 
        'due_date', 'description', 'amount', 'status', 'payment_id', 
        'year', 'month', 'created_at', 'updated_at'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(invoices)
    
    print(f"Generated {len(invoices)} invoices in {output_file}")
    print(f"({len(payment_templates)} invoices × {len(residents)} residents = {len(payment_templates) * len(residents)} total)")
    
    # Print summary by payment type
    print("\nInvoices by Payment Type:")
    for template in payment_templates:
        count = len([i for i in invoices if i['description'] == template['description']])
        print(f"  {template['description']}: {count} invoices (${template['amount']} each)")
    
    # Print summary by year
    year_counts = {}
    for invoice in invoices:
        year = invoice['year']
        year_counts[year] = year_counts.get(year, 0) + 1
    
    print("\nInvoices by Year:")
    for year in sorted(year_counts.keys()):
        print(f"  {year}: {year_counts[year]} invoices")

if __name__ == "__main__":
    # Generate invoices for all residents based on the 8 payment types
    generate_invoices_for_all_residents(
        'payments_rows-3.csv',  # The 8 payment templates
        'residents_unique_id.csv',  # All residents
        'invoices_for_all_residents.csv'  # Output file
    )
