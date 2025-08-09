import fitz  # PyMuPDF

import re

def is_likely_toc(text: str) -> bool:
    """
    Heuristic to check if the page contains a TOC-like structure:
    - multiple lines with dots and numbers (e.g., Chapter Title .......... 12)
    """
    lines = text.splitlines()
    toc_lines = 0

    for line in lines:
        if re.search(r'\.{3,}\s*\d+$', line):  # Look for lines ending in page numbers
            toc_lines += 1

    return toc_lines >= 5  # Arbitrary threshold


def extract_pdf_toc_smart(pdf_path: str):
    doc = fitz.open(pdf_path)

    # 1. Try bookmarks (TOC)
    toc = doc.get_toc()
    if toc:
        print("📑 Extracted Table of Contents from bookmarks:\n")
        for level, title, page in toc:
            indent = "  " * (level - 1)
            print(f"{indent}- {title} (Page {page})")
        return

    print("🔍 Scanning pages for a likely Table of Contents...\n")

    # 2. Scan for TOC structure heuristically
    for page_num in range(min(20, len(doc))):  # scan only first 20 pages
        page = doc[page_num]
        text = page.get_text()

        # Check if the page has a standalone "Table of Contents" or "Contents"
        lines = text.lower().splitlines()
        headings = [line.strip() for line in lines if len(line.strip()) < 40]

        if any(h in ["table of contents", "contents"] for h in headings) or is_likely_toc(text):
            print(f"📄 Likely TOC found on page {page_num + 1}:\n")
            print(text)
            return

    print("❌ Table of Contents not found.")

# === Example Usage ===
if __name__ == "__main__":
    pdf_path = "sample4.pdf"  # Replace with the path to your PDF
    extract_pdf_toc_smart(pdf_path)
