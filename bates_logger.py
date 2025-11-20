"""
bates_logger.py - Read a set of folders containing searchable PDFs to create a Bates log.

The script will ignore folders or files whose names start with a period ".". 
The PDFs must be searchable so you may have to run an OCR application to create searchable PDFs.
"""
import os
import re
import csv
import fitz
from pathlib import Path

BATES_PATTERN = (
    r'(?:'
    r'3rd Party Production\s*-\s*\d{6}|'
    r'MFLG XXX\s*\d{6}|'
    r'3rd Party\s*-\s*\d{6}|'
    r'\(2025-\d{2}\.\d{2}\)\s*\d{6}|'
    r'2025-\d{2}\.\d{2}\s*\d{6}|'
    r'JGS\s*\d{6}'
    r')'
)
BASE_DIRECTORY = r"Z:\Shared\Client Files\Plano\NAG\Schuler, Jill (Divorce) 40578 - RLR, TJD\Experts\Aaron Ballard"
OUTPUT_FILE = "bates_log.csv"


def extract_bates_numbers(pdf_path):
    """Extract first and last Bates numbers from a searchable PDF."""
    first_bates = None
    last_bates = None

    try:
        doc = fitz.open(pdf_path)

        # First page
        if len(doc) > 0:
            first_page = doc[0]
            first_text = first_page.get_text("text")
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
        print(f"Error reading {pdf_path}: {e}")

    return first_bates, last_bates


def path_contains_hidden_element(path: Path) -> bool:
    """
    Return True if any part of the path or the filename starts with a dot.
    """
    return any(part.startswith('.') for part in path.parts)


def process_file_list(file_list, output_csv):
    """Process list of file paths and create CSV with Bates numbers."""
    results = []

    for file_path in file_list:
        path_obj = Path(file_path)

        # Skip hidden files or files in hidden folders
        if path_contains_hidden_element(path_obj):
            print(f"Skipping hidden path: {file_path}")
            continue

        if not file_path.lower().endswith('.pdf'):
            continue

        if not path_obj.exists():
            print(f"File not found: {file_path}")
            continue

        filename = path_obj.name
        print(f"Processing: {filename}")

        first_bates, last_bates = extract_bates_numbers(file_path)
        results.append({
            'beginning_bates': first_bates or '',
            'ending_bates': last_bates or '',
            'filename': filename,
            'path': file_path
        })
        print(f"  First: {first_bates}, Last: {last_bates}")

    # Write to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['beginning_bates', 'ending_bates', 'filename', 'path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"\nResults written to: {output_csv}")


def read_file_list_from_txt(txt_file_path):
    """Read file paths from a text file (one path per line)."""
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip().endswith('.pdf')]


def scan_directory_for_pdfs(directory_path):
    """Recursively scan directory for PDF files, excluding hidden files and folders."""
    return [
        str(p)
        for p in Path(directory_path).rglob("*.pdf")
        if not path_contains_hidden_element(p)
    ]


if __name__ == "__main__":
    print("Bates Number Extraction Script")
    print("=" * 40)

    print("\nScanning directory for PDFs...")
    file_paths = scan_directory_for_pdfs(BASE_DIRECTORY)
    process_file_list(file_paths, OUTPUT_FILE)
