import os
import uuid
import logging
from typing import Dict, Any
from forms.renovation_form import RenovationForm
from services.document_generation.word_generator import WordGenerator
from services.document_generation.form_mapper import FormMapper
from services.document_generation.template_modifier import modify_template


class DocumentService:
    """
    Service for handling document generation.
    """

    def __init__(self, output_dir: str = "static/generated_docs"):
        """
        Initialize the DocumentService.

        Args:
            output_dir: Directory where generated documents will be stored
        """
        # Get the base directory (project root)
        self.base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Base directory: {self.base_dir}")

        # Use absolute paths
        self.output_dir = os.path.join(self.base_dir, output_dir)
        self.logger.debug(f"Output directory: {self.output_dir}")

        # Initialize word generator with absolute template path
        template_dir = os.path.join(self.base_dir, "templates", "word")
        self.word_generator = WordGenerator(template_dir=template_dir)

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Ensure the template with placeholders exists
        self.template_path = os.path.join(
            self.base_dir, "templates", "word", "renovation_quote_template.docx"
        )
        self.logger.debug(f"Template path: {self.template_path}")

        if not os.path.exists(self.template_path):
            try:
                # Check if the base template exists
                base_template = os.path.join(
                    self.base_dir, "templates", "word", "renovation_quote.docx"
                )
                self.logger.debug(f"Base template path: {base_template}")

                if not os.path.exists(base_template):
                    self.logger.error(f"Base template not found at: {base_template}")
                    self.logger.error(f"Current directory: {os.getcwd()}")
                    word_dir = os.path.join(self.base_dir, "templates", "word")
                    if os.path.exists(word_dir):
                        self.logger.error(f"Directory contents: {os.listdir(word_dir)}")
                    else:
                        self.logger.error(f"Word directory does not exist: {word_dir}")
                    raise FileNotFoundError(f"Base template not found: {base_template}")

                self.template_path = modify_template(base_dir=self.base_dir)
            except Exception as e:
                self.logger.error(f"Error creating template: {str(e)}")
                self.logger.error(f"Current directory: {os.getcwd()}")
                self.logger.error(f"Base directory: {self.base_dir}")
                templates_dir = os.path.join(self.base_dir, "templates")
                self.logger.error(
                    f"Templates directory exists: {os.path.exists(templates_dir)}"
                )
                if os.path.exists(templates_dir):
                    word_dir = os.path.join(templates_dir, "word")
                    self.logger.error(
                        f"Word directory exists: {os.path.exists(word_dir)}"
                    )
                    if os.path.exists(word_dir):
                        self.logger.error(
                            f"Files in templates/word: {os.listdir(word_dir)}"
                        )
                raise RuntimeError(f"Failed to create template: {str(e)}")

    def generate_renovation_quote(self, form: RenovationForm) -> str:
        """
        Generate a renovation quote document from the form data.

        Args:
            form: The submitted form with data

        Returns:
            The path to the generated document
        """
        try:
            # Map form data to template variables
            context = FormMapper.map_form_to_template(form)

            # Generate a unique filename
            filename = f"renovation_quote_{uuid.uuid4().hex}.docx"
            output_path = os.path.join(self.output_dir, filename)

            # Generate the document
            return self.word_generator.generate_document(
                template_name="renovation_quote_template.docx",
                context=context,
                output_path=output_path,
            )
        except Exception as e:
            self.logger.error(f"Error generating document: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to generate document: {str(e)}")
