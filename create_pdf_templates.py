import os


def main():
    """
    Create necessary directories for PDF generation.
    We don't need actual template files anymore since we're generating PDFs directly.
    """
    # Ensure template directory exists
    os.makedirs("templates/pdf", exist_ok=True)

    # Ensure output directory exists
    os.makedirs("static/generated_docs", exist_ok=True)

    print("PDF directories created successfully!")


if __name__ == "__main__":
    main()
