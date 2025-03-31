from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    send_file,
    jsonify,
)
from forms.renovation_form import RenovationForm
from flask_wtf.csrf import CSRFProtect, generate_csrf
from services.document_generation.document_service import DocumentService
from services.document_generation.pdf_generator import PDFGenerator
from services.database import Database
import logging
import secrets
import os
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Generate a strong random secret key
app.config["SECRET_KEY"] = secrets.token_hex(16)  # More secure random key
app.config["WTF_CSRF_ENABLED"] = False  # Temporarily disable CSRF for testing
app.config["WTF_CSRF_TIME_LIMIT"] = 3600  # Extend CSRF token validity to 1 hour
app.config["WTF_CSRF_SSL_STRICT"] = False  # Less strict SSL checking for development

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize document service
document_service = DocumentService()

# Initialize PDF generator
pdf_generator = PDFGenerator()

# Initialize database
db = Database()


# Make CSRF token available in all templates
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf)


# Log the application startup
logger.info("Application starting with CSRF protection disabled for testing")


@app.route("/", methods=["GET", "POST"])
def index():
    form = RenovationForm()
    logger.debug("Form request method: %s", request.method)

    # For debugging, print form data
    if request.method == "POST":
        logger.debug("Form data: %s", request.form)
        # Check if csrf_token is in the form data
        if "csrf_token" in request.form:
            logger.debug(
                "CSRF token found in form data: %s", request.form.get("csrf_token")
            )
        else:
            logger.warning("No CSRF token in form data!")

        # Log all form fields to see what's being submitted
        logger.debug("==== FORM SUBMISSION DETAILS ====")
        for field_name, field_value in request.form.items():
            logger.debug("Field: %s, Value: %s", field_name, field_value)
        logger.debug("==== END FORM SUBMISSION DETAILS ====")

        # Modified validation to handle CSRF token issues
        if request.method == "POST":
            logger.debug("Processing POST request")

            # Set default values for required fields
            form.set_defaults()

            # Use either validate_on_submit() or validate() depending on CSRF setting
            if app.config["WTF_CSRF_ENABLED"]:
                form_valid = form.validate_on_submit()
            else:
                form_valid = form.validate()

            if form_valid:
                logger.debug("Form validated successfully")

                try:
                    # Generate Word document
                    document_path = document_service.generate_renovation_quote(form)
                    logger.debug("Generated document at: %s", document_path)

                    # Generate PDF workorders
                    workorder_paths = []
                    try:
                        workorder_paths = pdf_generator.generate_all_workorders(form)
                        logger.debug(f"Generated {len(workorder_paths)} workorder PDFs")
                    except Exception as pdf_error:
                        logger.error(
                            f"Error generating workorder PDFs: {str(pdf_error)}"
                        )
                        # Don't fail the form submission if workorder PDFs fail
                        flash(
                            "Warning: Could not generate workorder PDFs. The main quote was still created.",
                            "warning",
                        )

                    # Store the document path in session for download
                    filename = os.path.basename(document_path)

                    # Save form data to database
                    customer_name = f"{form.personal_details.first_name.data} {form.personal_details.last_name.data}"
                    email = form.personal_details.email.data
                    phone = form.personal_details.phone.data
                    address = form.personal_details.address.data
                    floor_area = (
                        float(form.bathroom_details.floor_area.data)
                        if form.bathroom_details.floor_area.data
                        else 0
                    )

                    # Convert form data to a dictionary for storage
                    form_data = {}
                    for field_name, field_value in request.form.items():
                        form_data[field_name] = field_value

                    # Store workorder filenames in the database
                    workorder_filenames = [
                        os.path.basename(path) for path in workorder_paths
                    ]

                    # Add to database - store just the filename, not the full path
                    quote_id = db.add_quote(
                        customer_name=customer_name,
                        email=email,
                        phone=phone,
                        address=address,
                        floor_area=floor_area,
                        document_path=filename,  # Store only the filename
                        form_data=form_data,
                        workorder_paths=workorder_filenames,  # Add workorder filenames
                    )

                    logger.debug(f"Saved quote to database with ID: {quote_id}")

                    # Prepare success message with download links
                    success_msg = f"Form submitted successfully. <a href='{url_for('download_document', filename=filename)}'>Download Quote</a>"

                    # Add workorder download links if they were generated
                    if workorder_paths:
                        success_msg += "<br>Workorder PDFs: "
                        for i, path in enumerate(workorder_paths):
                            work_type = (
                                ["Electrician", "Plumber", "Carpenter"][i]
                                if i < 3
                                else f"Workorder {i+1}"
                            )
                            path_filename = os.path.basename(path)
                            success_msg += f"<a href='{url_for('download_document', filename=path_filename)}'>{work_type}</a> "

                    flash(success_msg, "success")

                except Exception as e:
                    logger.exception("Error generating document: %s", str(e))
                    error_details = str(e)
                    tb = traceback.format_exc()
                    logger.error("Traceback: %s", tb)

                    # Provide a more user-friendly error message
                    flash(
                        "An error occurred while generating the document. Please try again or contact support.",
                        "danger",
                    )

                return redirect(url_for("index"))
            else:
                # If form validation failed, log validation errors
                logger.debug("Form validation failed")

                # Check for extra_items validation issues and try to fix them
                if "additional_notes" in form._fields and hasattr(
                    form.additional_notes, "extra_items"
                ):
                    logger.debug("Checking extra_items field")
                    # If extra_items is causing validation issues, try to provide a default value
                    if not form.additional_notes.extra_items.data:
                        logger.debug("No extra_items data, providing default")
                        # Create a default empty item
                        form.additional_notes.extra_items.data = [
                            {"item": "", "cost": 0}
                        ]
                        # Try validation again
                        if app.config["WTF_CSRF_ENABLED"]:
                            form_valid = form.validate_on_submit()
                        else:
                            form_valid = form.validate()

                        if form_valid:
                            logger.debug(
                                "Form validated successfully after fixing extra_items"
                            )
                            flash("Form submitted successfully", "success")
                            return redirect(url_for("index"))

                # Log all form errors in a more structured way
                logger.debug("==== FORM VALIDATION ERRORS ====")
                for fieldname, errors in form.errors.items():
                    logger.debug("Validation error in %s: %s", fieldname, errors)

                # Log nested form errors for each form section
                for section in [
                    "personal_details",
                    "bathroom_details",
                    "appliances",
                    "interior_fittings",
                    "tiles_and_painting",
                    "additional_notes",
                ]:
                    section_form = getattr(form, section)
                    if section_form.errors:
                        for fieldname, errors in section_form.errors.items():
                            logger.debug(
                                "Validation error in %s: %s",
                                f"{section}.{fieldname}",
                                errors,
                            )

                            # For FieldList errors, provide more details
                            if (
                                fieldname == "extra_items"
                                and section == "additional_notes"
                            ):
                                logger.debug(
                                    "Extra items data structure: %s",
                                    type(section_form.extra_items),
                                )
                                logger.debug(
                                    "Extra items errors: %s",
                                    section_form.extra_items.errors,
                                )

                                # Try to access the data to see what's there
                                try:
                                    logger.debug(
                                        "Extra items data: %s",
                                        section_form.extra_items.data,
                                    )
                                    for i, item_data in enumerate(
                                        section_form.extra_items.data
                                    ):
                                        logger.debug(
                                            "Extra item %d data: %s", i, item_data
                                        )
                                except Exception as e:
                                    logger.exception(
                                        "Error accessing extra_items data: %s", str(e)
                                    )

                logger.debug("==== END FORM VALIDATION ERRORS ====")

                # For debugging purposes, let's check if there's a CSRF error specifically
                if "csrf_token" in form.errors:
                    logger.error(
                        "CSRF Token validation failed: %s", form.errors["csrf_token"]
                    )

                # Check if the form data contains the CSRF token
                if "csrf_token" in request.form:
                    logger.debug(
                        "CSRF token found in form data: %s",
                        request.form.get("csrf_token"),
                    )
                else:
                    logger.error("No CSRF token in form data")

                # Flash a message to inform the user
                flash("Please fill in all required fields correctly", "danger")

    return render_template("index.html", form=form)


@app.route("/quotes")
def quotes():
    """
    Display all quotes in the database.
    """
    quotes_list = db.get_all_quotes()
    return render_template("quotes.html", quotes=quotes_list)


@app.route("/quotes/<int:quote_id>")
def quote_details(quote_id):
    """
    Display details for a specific quote.
    """
    quote = db.get_quote_by_id(quote_id)
    if not quote:
        flash("Quote not found", "danger")
        return redirect(url_for("quotes"))

    return render_template("quote_details.html", quote=quote)


@app.route("/quotes/delete/<int:quote_id>", methods=["POST"])
def delete_quote(quote_id):
    """
    Delete a quote from the database.
    """
    try:
        # Get the quote to find the document path
        quote = db.get_quote_by_id(quote_id)
        if not quote:
            flash("Quote not found", "danger")
            return redirect(url_for("quotes"))

        # Delete the document file if it exists
        document_path = quote.get("document_path")
        if document_path:
            # Construct the full path to the document
            full_path = os.path.join(document_service.output_dir, document_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                logger.debug(f"Deleted document file: {full_path}")

        # Delete any workorder PDF files if they exist
        workorder_paths = quote.get("workorder_paths", [])
        for workorder_path in workorder_paths:
            # Construct the full path to the workorder PDF
            full_path = os.path.join(pdf_generator.output_dir, workorder_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                logger.debug(f"Deleted workorder PDF file: {full_path}")

        # Delete from database
        success = db.delete_quote(quote_id)

        if success:
            flash("Quote deleted successfully", "success")
        else:
            flash("Failed to delete quote", "danger")

    except Exception as e:
        logger.exception(f"Error deleting quote: {str(e)}")
        flash("An error occurred while deleting the quote", "danger")

    return redirect(url_for("quotes"))


@app.route("/download/<filename>")
def download_document(filename):
    """
    Route for downloading generated documents.

    Args:
        filename: The filename of the document to download

    Returns:
        The document file for download
    """
    try:
        # Determine if this is a PDF workorder or a Word quote
        is_pdf = filename.endswith(".pdf")

        # Select the appropriate directory
        if is_pdf:
            file_dir = pdf_generator.output_dir
            download_name = filename  # Keep the original name for PDFs
        else:
            file_dir = document_service.output_dir
            download_name = "renovation_quote.docx"  # Default name for Word docs

        # Construct the full path to the document
        file_path = os.path.join(file_dir, filename)
        logger.debug(f"Attempting to download document: {file_path}")

        if not os.path.exists(file_path):
            logger.error(f"Document not found: {file_path}")
            flash(
                "Document not found. Please try generating the quote again.", "danger"
            )
            return redirect(url_for("index"))

        return send_file(file_path, as_attachment=True, download_name=download_name)
    except Exception as e:
        logger.exception(f"Error downloading document: {str(e)}")
        flash(
            "An error occurred while downloading the document. Please try again.",
            "danger",
        )
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
