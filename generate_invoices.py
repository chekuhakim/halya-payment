#!/usr/bin/env python3
"""
Generate invoices from payments data for Halya Payment System
Converts payment records into invoice records with appropriate dates and status
"""

import csv
import datetime
from typing import List, Dict
import random

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

def determine_invoice_status(description: str, year: int) -> str:
    """Determine if invoice should be PAID, PENDING, or OVERDUE"""
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    
    if 'guard fee' in description.lower():
        month = parse_month_from_description(description)
        if month and year == current_year and month < current_month:
            return 'PAID'  # Past months are likely paid
        elif month and year == current_year and month == current_month:
            return 'PENDING'  # Current month
        elif month and year == current_year and month > current_month:
            return 'PENDING'  # Future months
        elif year < current_year:
            return 'PAID'  # Past years are likely paid
    else:
        # Annual/Membership fees
        if year < current_year:
            return 'PAID'
        elif year == current_year:
            return 'PENDING'
    
    return 'PENDING'

def generate_invoices_from_payments(payments_file: str, output_file: str):
    """Generate invoices CSV from payments data"""
    
    invoices = []
    invoice_id = 1
    
    with open(payments_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            resident_id = row['resident_id']
            description = row['description']
            amount = float(row['amount'])
            year = int(row['year'])
            
            # Skip empty rows
            if not resident_id or not description:
                continue
            
            # Parse month from description
            month = parse_month_from_description(description)
            
            # Generate dates
            invoice_date = generate_invoice_date(year, month)
            due_date = generate_due_date(invoice_date, description)
            
            # Determine status
            status = determine_invoice_status(description, year)
            
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
    
    # Print summary
    status_counts = {}
    for invoice in invoices:
        status = invoice['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\nInvoice Status Summary:")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")
    
    # Print by year
    year_counts = {}
    for invoice in invoices:
        year = invoice['year']
        year_counts[year] = year_counts.get(year, 0) + 1
    
    print("\nInvoices by Year:")
    for year in sorted(year_counts.keys()):
        print(f"  {year}: {year_counts[year]}")

if __name__ == "__main__":
    # Generate invoices from the main payments file
    generate_invoices_from_payments(
        'payments_unique_id.csv', 
        'invoices_generated.csv'
    )
