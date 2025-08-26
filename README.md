# Bates Number Extractor

A Python script for extracting Bates numbers from PDF discovery documents and organizing them into a structured CSV format. This tool is designed for legal professionals who need to efficiently catalog and manage large volumes of discovery documents with embedded Bates numbering.

## Overview

During legal discovery, documents are often produced with Bates numbers (unique identifiers) stamped on each page. These numbers may be embedded in different layers of the PDF (footers, annotations, stamps) and are not always reflected in the filename. This script extracts the first and last Bates numbers from each PDF file and outputs the results to a CSV file for easy import into case management systems.

## Features

- **Comprehensive Text Extraction**: Uses multiple extraction methods to find Bates numbers in different PDF layers (standard text, annotations, footer regions, character-level extraction)
- **Flexible Input Options**: Process files from hardcoded lists, text files, or directory scanning
- **Hidden Directory Filtering**: Automatically excludes directories starting with "." (following Linux convention)
- **Range Detection**: Identifies first and last Bates numbers for multi-page documents
- **Error Handling**: Continues processing even when individual files encounter issues
- **CSV Output**: Generates structured data ready for import into legal case management systems

## Requirements

- Python 3.6+
- pymupdf library

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
cd bates-number-extractor
```

2. Install required dependencies:
```bash
pip install pymupdf
```

## Usage

### Variables to Set

The following variables control the ooperation of the script:

* BATES_PATTERN: Regular expression for locating the Bates number.
* BASE_DIRECTORY: Folder to start searching for PDFs (if using the option to scan a folder and subfolders)
* OUTPUT_FILE: Name of the output CSV file that will contiain a list of files scanned along with their beginning and ending Bates numbers

### Basic Usage

Update the `file_list` variable with your PDF file paths and run:

```bash
python bates_extractor.py
```

### Input Options

#### Option 1: Hardcoded File List
Modify the `file_list` variable in the script with your file paths:
```python
file_list = [
    r"C:\path\to\document1.pdf",
    r"C:\path\to\document2.pdf",
    # Add more files...
]
```

#### Option 2: Directory Scanning
Scan a directory recursively for all PDF files:
```python
BASE_DIRECTORY = r"C:\path\to\discovery\documents"
file_paths = scan_directory_for_pdfs(base_directory)
process_file_list(file_paths, OUTPUT_FILE)
```

## Bates Number Pattern

The script searches for Bates numbers matching the pattern: `TJD######` (where # represents digits). To modify for different patterns, update the `BATES_PATTERN` variable:

```python
BATES_PATTERN = r'TJD\d{6}'  # Current pattern: TJD followed by 6 digits
```

## Output Format

The script generates a CSV file with the following columns:
- `beginning_bates`: First Bates number found in the document
- `ending_bates`: Last Bates number found in the document  
- `filename`: Name of the PDF file (without path)

Example output:
```csv
beginning_bates,ending_bates,filename
TJD000001,TJD000005,Discovery_Production.pdf
TJD000010,TJD000010,Expert_Report.pdf
TJD000025,TJD000030,Bank_Statements.pdf
```

## Error Handling

The script includes comprehensive error handling:
- Skips non-existent files with warnings
- Continues processing if individual PDFs encounter errors
- Reports processing status for each file
- Logs errors without stopping the entire process

## Advanced Features

### Multiple Extraction Methods
The script attempts several extraction techniques:
1. Standard text extraction
2. Simple text extraction (alternative algorithm)
3. Footer region extraction (bottom 10% of page)
4. Annotations and stamps extraction
5. Character-level extraction

### Hidden Directory Filtering
When scanning directories, the script automatically excludes any directories starting with "." to avoid processing hidden system folders.

## Troubleshooting

**Bates numbers not found**: If Adobe Acrobat can find the numbers but the script cannot, the numbers may be in annotations or stamps. The script's comprehensive extraction methods should handle most cases.

**Memory issues with large files**: For very large PDF files, consider processing in smaller batches.

**Path issues on Windows**: Use raw strings (prefix with `r`) for Windows file paths to handle backslashes correctly.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Thomas J. Daley** is a family law litigation attorney practicing primarily in Collin County, Texas and representing clients in family disputes throughout the State of Texas and the United States. As a tech entrepreneur, he leverages AI to bring high-quality legal services that work better, faster, and cheaper than traditional approaches to resolving cases.
