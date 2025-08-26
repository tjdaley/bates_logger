"""
bates_logger.py - Read a set of folders containing searchable PDFs to create a Bates log.

The script will ignore folders whose names start with a period ".". The PDFs must be searchable so you may have to run an OCR application to create searchable PDFs.
"""
import os
import re
import csv
import fitz
from pathlib import Path

BATES_PATTERN = r'DTB \d{4}'
BASE_DIRECTORY = r"c:\path\to\your\root\folder"
OUTPUT_FILE = "bates_log.csv"

def extract_bates_numbers(pdf_path):
    """Alternative extraction using PyMuPDF"""
    first_bates = None
    last_bates = None
    
    try:
        doc = fitz.open(pdf_path)
        
        # First page
        if len(doc) > 0:
            first_page = doc[0]
            first_text = first_page.get_text("text")  # or try "dict", "json"

            first_matches = re.findall(BATES_PATTERN, first_text)
            if first_matches:
                first_bates = first_matches[0]
        
        # Last page  
        if len(doc) > 0:
            last_page = doc[-1]
            last_text = last_page.get_text("text")
            last_matches = re.findall(BATES_PATTERN, last_text)
            if last_matches:
                last_bates = last_matches[-1]
                
        doc.close()
    except Exception as e:
        print(f"Error with PyMuPDF: {e}")
    
    return first_bates, last_bates

def process_file_list(file_list, output_csv):
    """
    Process list of file paths and create CSV with bates numbers.
    """
    results = []
    
    for file_path in file_list:
        print(f"Processing: {file_path}")
        # Skip if not a PDF file
        if not file_path.lower().endswith('.pdf'):
            continue
            
        # Skip if file doesn't exist
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
            
        # Extract filename without path
        filename = os.path.basename(file_path)
        
        print(f"Processing: {filename}")
        
        # Extract bates numbers
        first_bates, last_bates = extract_bates_numbers(file_path)
        
        # Add to results
        results.append({
            'beginning_bates': first_bates or '',
            'ending_bates': last_bates or '',
            'filename': filename
        })
        
        print(f"  First: {first_bates}, Last: {last_bates}")
    
    # Write to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['beginning_bates', 'ending_bates', 'filename']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    
    print(f"\nResults written to: {output_csv}")

def read_file_list_from_txt(txt_file_path):
    """
    Read file paths from a text file (one path per line)
    """
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and line.strip().endswith('.pdf')]

def scan_directory_for_pdfs(directory_path):
    """
    Recursively scan directory for PDF files, excluding hidden directories (starting with .)
    """
    return [str(p) for p in Path(directory_path).rglob("*.pdf") if not any(part.startswith('.') for part in p.parts)]

# Usage examples:
if __name__ == "__main__":
    print("Bates Number Extraction Script")
    print("="*40)
    
    # Option 1: Read from a text file containing the file paths
    # Uncomment the lines below to use this option
    # print("\nOption 2: Reading from text file")
    # file_paths = read_file_list_from_txt("file_list.txt")
    # process_file_list(file_paths, OUTPUT_FILE)
    
    # Option 2: Scan a directory recursively for PDFs
    # Uncomment the lines below to use this option
    print("\nOption 3: Scanning directory")
    
    file_paths = scan_directory_for_pdfs(BASE_DIRECTORY)
    process_file_list(file_paths, OUTPUT_FILE)
