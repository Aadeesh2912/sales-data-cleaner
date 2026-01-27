#!/usr/bin/env python3
"""
Sales Data Cleaner
Reads sales CSV, cleans it, removes duplicates, converts USD to INR, and saves as JSON.
"""

import csv
import json


def clean_field(field):
    """Remove quotes, dollar signs, and extra whitespace from a field."""
    return field.strip().replace('"', '').replace('$', '')


def read_and_clean_csv(filepath):
    """Read the CSV file and clean each field."""
    cleaned_data = []
    
    with open(filepath, 'r') as file:
        csv_reader = csv.reader(file)
        
        for row in csv_reader:
            # Skip empty rows
            if not row:
                continue
            
            # Clean each field
            product_id = clean_field(row[0])
            product_name = clean_field(row[1])
            price_str = clean_field(row[2])
            country = clean_field(row[3])
            
            # Convert price to float
            try:
                price = float(price_str)
            except ValueError:
                print(f"Warning: Couldn't convert price '{price_str}' to number. Skipping this row.")
                continue
            
            cleaned_data.append({
                'product_id': product_id,
                'product_name': product_name,
                'price_usd': price,
                'country': country
            })
    
    return cleaned_data


def remove_duplicates(data):
    """Remove rows with the same product name and price."""
    seen = set()
    unique_data = []
    
    for record in data:
        # Use product name and price as the key for duplicate detection
        key = (record['product_name'], record['price_usd'])
        
        if key not in seen:
            seen.add(key)
            unique_data.append(record)
    
    return unique_data


def convert_to_inr(data, rate=83.0):
    """Convert all prices from USD to INR."""
    for record in data:
        record['price_inr'] = round(record['price_usd'] * rate, 2)
        # Remove the USD price since we have INR now
        del record['price_usd']
    
    return data


def save_to_json(data, filepath):
    """Save the cleaned data to a JSON file."""
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)
    
    print(f"✓ Saved {len(data)} records to {filepath}")


def main():
    """Main function that runs the entire pipeline."""
    print("=" * 50)
    print("Sales Data Cleaner")
    print("=" * 50)
    
    input_file = 'sales.csv'
    output_file = 'clean_sales.json'
    
    # Step 1: Read and clean the CSV
    print(f"\n1. Reading {input_file}...")
    cleaned_data = read_and_clean_csv(input_file)
    print(f"   ✓ Loaded {len(cleaned_data)} records")
    
    # Step 2: Remove duplicates
    print(f"\n2. Removing duplicates...")
    unique_data = remove_duplicates(cleaned_data)
    removed = len(cleaned_data) - len(unique_data)
    print(f"   ✓ Removed {removed} duplicate(s)")
    print(f"   ✓ {len(unique_data)} unique records left")
    
    # Step 3: Convert USD to INR
    print(f"\n3. Converting prices to INR (1 USD = 83 INR)...")
    final_data = convert_to_inr(unique_data)
    print(f"   ✓ Converted all prices")
    
    # Step 4: Save to JSON
    print(f"\n4. Saving to {output_file}...")
    save_to_json(final_data, output_file)
    
    print("\n" + "=" * 50)
    print("Done! Check clean_sales.json")
    print("=" * 50)


if __name__ == "__main__":
    main()
