import os
import sys
import io
from pikepdf import Pdf
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pdfrw import PdfReader as PdfrwReader
import fitz  # PyMuPDF


def inspect_pdf_with_pikepdf(pdf_path):
    print(f"\n=== Inspecting {pdf_path} with pikepdf ===")
    pdf = Pdf.open(pdf_path)

    # Check if this PDF has a form
    root = pdf.Root
    if hasattr(root, "AcroForm"):
        print("This PDF has a form (AcroForm)")
        if "Fields" in root.AcroForm:
            fields = root.AcroForm.Fields
            print(f"Number of form fields: {len(fields)}")
            for i, field in enumerate(fields):
                print(f"Field {i}: {field}")
                if hasattr(field, "T"):
                    print(f"  Name: {field.T}")
                if hasattr(field, "FT"):
                    print(f"  Type: {field.FT}")
    else:
        print("This PDF does not have a form (AcroForm)")


def inspect_pdf_with_pypdf2(pdf_path):
    print(f"\n=== Inspecting {pdf_path} with PyPDF2 ===")
    reader = PdfReader(pdf_path)

    # Check for forms
    form_fields = reader.get_fields()
    if form_fields:
        print(f"Form fields: {form_fields}")
    else:
        print("No form fields found")

    # Extract text from first page
    page = reader.pages[0]
    text = page.extract_text()
    print(f"First page text (first 200 chars): {text[:200]}")


def inspect_pdf_with_pdfrw(pdf_path):
    print(f"\n=== Inspecting {pdf_path} with pdfrw ===")
    reader = PdfrwReader(pdf_path)

    # Check for annotations which might be form fields
    for i, page in enumerate(reader.pages):
        if page.Annots:
            print(f"Page {i+1} has {len(page.Annots)} annotations")
            for j, annot in enumerate(page.Annots):
                print(f"  Annotation {j}: {annot}")
                if hasattr(annot, "T"):
                    print(f"    Field name: {annot.T}")
                if hasattr(annot, "FT"):
                    print(f"    Field type: {annot.FT}")


def inspect_pdf_with_pymupdf(pdf_path):
    print(f"\n=== Inspecting {pdf_path} with PyMuPDF ===")
    doc = fitz.open(pdf_path)

    # Check for forms - updated for newer PyMuPDF versions
    form_fields = {}
    for widget in doc.widgets():
        field_name = widget.field_name
        field_type = widget.field_type
        field_value = widget.field_value
        if field_name:
            form_fields[field_name] = {"type": field_type, "value": field_value}

    if form_fields:
        print(f"Form fields: {form_fields}")
    else:
        print("No form fields found")

    # Extract text from first page
    text = doc[0].get_text()
    print(f"First page text (first 200 chars): {text[:200]}")

    # Check page dimensions
    print(f"Page count: {doc.page_count}")
    print(
        f"First page dimensions: width={doc[0].rect.width}, height={doc[0].rect.height}"
    )

    # Look for annotations
    for i in range(doc.page_count):
        page = doc[i]
        annots = page.annots()
        if annots:
            print(f"Page {i+1} has {len(annots)} annotations")
            for j, annot in enumerate(annots):
                print(f"  Annotation {j}: {annot.type}, rect={annot.rect}")


def test_pdf_form_filling(pdf_path, output_path):
    """Test creating a new PDF with filled-in form fields"""
    print(f"\n=== Testing form filling for {pdf_path} ===")

    # Create a simple PDF with text
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.setFont("Helvetica", 10)

    # Add some text to the PDF at specific positions
    c.drawString(100, 750, "Customer Name: John Doe")
    c.drawString(100, 730, "Address: 123 Main St")
    c.drawString(100, 710, "Phone: 555-1234")
    c.drawString(100, 690, "Email: john@example.com")

    c.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)

    try:
        # Create a new PDF using the original as template
        existing_pdf = PdfReader(pdf_path)
        output_pdf_writer = PdfWriter()

        # Add page from original PDF
        output_pdf_writer.add_page(existing_pdf.pages[0])

        # Merge in the new content
        new_pdf = PdfReader(packet)
        page = output_pdf_writer.pages[0]
        page.merge_page(new_pdf.pages[0])

        # Write the output PDF
        with open(output_path, "wb") as output_file:
            output_pdf_writer.write(output_file)

        print(f"Successfully created PDF at {output_path}")
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")


def test_pdf_form_filling_with_pymupdf(pdf_path, output_path):
    """Test creating a new PDF with filled-in text using PyMuPDF"""
    print(f"\n=== Testing form filling with PyMuPDF for {pdf_path} ===")

    try:
        # Open the PDF
        doc = fitz.open(pdf_path)

        # Get the first page
        page = doc[0]

        # Add text to the page
        rect = fitz.Rect(100, 100, 400, 120)  # x0, y0, x1, y1
        page.insert_textbox(
            rect,
            "Customer Name: John Doe",
            fontsize=12,
            fontname="helv",
            color=(0, 0, 0),
        )

        rect = fitz.Rect(100, 130, 400, 150)
        page.insert_textbox(
            rect, "Address: 123 Main St", fontsize=12, fontname="helv", color=(0, 0, 0)
        )

        rect = fitz.Rect(100, 160, 400, 180)
        page.insert_textbox(
            rect, "Phone: 555-1234", fontsize=12, fontname="helv", color=(0, 0, 0)
        )

        rect = fitz.Rect(100, 190, 400, 210)
        page.insert_textbox(
            rect,
            "Email: john@example.com",
            fontsize=12,
            fontname="helv",
            color=(0, 0, 0),
        )

        # Save the PDF
        doc.save(output_path)
        print(f"Successfully created PDF at {output_path}")
    except Exception as e:
        print(f"Error creating PDF with PyMuPDF: {str(e)}")


def main():
    # PDF files to inspect
    pdf_paths = [
        "templates/pdf/electriciatian.pdf",
        "templates/pdf/plumber.pdf",
        "templates/pdf/carpenter.pdf",
    ]

    # Create output directory
    os.makedirs("output", exist_ok=True)

    try:
        # Try to inspect with PyMuPDF
        for pdf_path in pdf_paths:
            inspect_pdf_with_pymupdf(pdf_path)
    except ImportError:
        print("PyMuPDF (fitz) not installed, skipping that inspection")
    except Exception as e:
        print(f"Error with PyMuPDF inspection: {str(e)}")

    for pdf_path in pdf_paths:
        try:
            inspect_pdf_with_pikepdf(pdf_path)
        except Exception as e:
            print(f"Error with pikepdf inspection: {str(e)}")

        try:
            inspect_pdf_with_pypdf2(pdf_path)
        except Exception as e:
            print(f"Error with PyPDF2 inspection: {str(e)}")

        try:
            inspect_pdf_with_pdfrw(pdf_path)
        except Exception as e:
            print(f"Error with pdfrw inspection: {str(e)}")

        # Test form filling
        output_path = os.path.join(
            "output", f"test_pypdf2_{os.path.basename(pdf_path)}"
        )
        try:
            test_pdf_form_filling(pdf_path, output_path)
        except Exception as e:
            print(f"Error testing form filling: {str(e)}")

        # Test form filling with PyMuPDF
        output_path = os.path.join(
            "output", f"test_pymupdf_{os.path.basename(pdf_path)}"
        )
        try:
            test_pdf_form_filling_with_pymupdf(pdf_path, output_path)
        except Exception as e:
            print(f"Error testing form filling with PyMuPDF: {str(e)}")


if __name__ == "__main__":
    main()
