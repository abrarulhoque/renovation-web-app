import fitz  # PyMuPDF
import os


def list_pdf_form_fields(pdf_path):
    """
    List all form fields in a PDF document
    """
    print(f"\nChecking form fields in {pdf_path}...")
    try:
        doc = fitz.open(pdf_path)
        form_fields = []

        for page_num, page in enumerate(doc):
            # Convert generator to list
            widgets = list(page.widgets())
            if not widgets:
                print(f"Page {page_num}: No form fields found")
            else:
                print(f"Page {page_num}: Found {len(widgets)} form fields")
                for widget in widgets:
                    field_info = {
                        "page": page_num,
                        "name": widget.field_name,
                        "type": widget.field_type_string,
                        "value": widget.field_value,
                        "rect": widget.rect,
                        "field_type": widget.field_type,
                    }
                    form_fields.append(field_info)
                    print(
                        f"  - Field: {widget.field_name} (Type: {widget.field_type_string})"
                    )

        if not form_fields:
            print("No form fields found in the document")
        else:
            print(f"Found {len(form_fields)} form fields in total")

        doc.close()
        return form_fields
    except Exception as e:
        print(f"Error inspecting PDF: {str(e)}")
        return []


def check_pdf_structure(pdf_path):
    """
    Check the general structure of the PDF file
    """
    print(f"\nInspecting PDF structure for {pdf_path}...")
    try:
        doc = fitz.open(pdf_path)
        print(f"Number of pages: {len(doc)}")

        # Get document metadata
        metadata = doc.metadata
        print(f"Title: {metadata.get('title', 'Not specified')}")
        print(f"Author: {metadata.get('author', 'Not specified')}")

        # Check first page content to see what we're working with
        page = doc[0]
        text = page.get_text()
        print(f"Text content preview (first 100 chars): {text[:100]}")

        # Check if the document has XFA (XML Forms Architecture)
        has_xfa = doc.xref_get_key(-1, "XFA")
        if has_xfa[0]:
            print("Document has XFA forms")
        else:
            print("Document doesn't have XFA forms")

        # Check if the document has AcroForm
        has_acroform = doc.xref_get_key(-1, "AcroForm")
        if has_acroform[0]:
            print("Document has AcroForm")
        else:
            print("Document doesn't have AcroForm")

        doc.close()
    except Exception as e:
        print(f"Error checking PDF structure: {str(e)}")


def main():
    template_dir = os.path.join("templates", "pdf")

    # List of PDF templates to check
    pdf_files = [
        os.path.join(template_dir, "electriciatian.pdf"),
        os.path.join(template_dir, "plumber.pdf"),
        os.path.join(template_dir, "carpenter.pdf"),
    ]

    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            check_pdf_structure(pdf_file)
            list_pdf_form_fields(pdf_file)
        else:
            print(f"File not found: {pdf_file}")


if __name__ == "__main__":
    main()
