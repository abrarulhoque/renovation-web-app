# Work Order PDF Templates

## Overview

This document explains how the workorder PDF generation works with custom templates. The system now uses pre-designed PDF templates stored in the `templates/pdf/` directory and overlays them with dynamically generated checkboxes and values from the submitted form.

## Template Files

The system uses three template files:

1. `templates/pdf/electriciatian.pdf` - Template for electrician workorders
2. `templates/pdf/plumber.pdf` - Template for plumber workorders
3. `templates/pdf/carpenter.pdf` - Template for carpenter workorders

## How It Works

The `PDFGenerator` class in `services/document_generation/pdf_generator.py` handles the generation of PDF workorders:

1. The system loads the appropriate template file based on the workorder type.
2. It then overlays the template with checkboxes (☑/☐) and values for each relevant field.
3. The checkboxes are placed in a two-column layout starting below the title area of the template.

## Template Requirements

Your template files should:

1. Have a clear title area at the top of the document
2. Allow space below the title (starting at approximately Y position 150) for the dynamically added checkboxes
3. Maintain a clean, consistent design that works well with the overlaid content

## PDF Generation Process

When a form is submitted, the system:

1. Creates copies of the template files
2. Processes the form data to determine what options are selected
3. Overlays checkmarks and values onto the templates using PyMuPDF
4. Saves the resulting PDF files in the `static/generated_docs/` directory
5. Provides download links for the generated PDF files

## Customizing Templates

To customize the templates:

1. Replace the existing PDF files in `templates/pdf/` with your own designs
2. The templates should be designed in a way that allows for the dynamic content to be added below the title area
3. You may need to adjust the starting Y position and other layout parameters in the `_generate_pdf` method if your template design differs significantly

## Troubleshooting

If the generated PDFs don't look correct:

1. Check that your template files are accessible and valid PDFs
2. Verify that there's enough space in your templates for the dynamic content
3. Adjust the positioning variables in the `_generate_pdf` method if needed:
   - `y_position` - Starting Y position for the checkboxes
   - `x_positions` - X positions for the two columns
   - `line_height` - Height of each line of text
