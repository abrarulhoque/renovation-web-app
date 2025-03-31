from docxtpl import DocxTemplate
import os
import logging
from typing import Dict, Any


class WordGenerator:
    """
    Class for generating Word documents from templates using docxtpl.
    """

    def __init__(self, template_dir: str = "templates/word"):
        """
        Initialize the WordGenerator with the template directory.

        Args:
            template_dir: Directory where Word templates are stored
        """
        self.template_dir = template_dir
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Template directory: {self.template_dir}")

    def generate_document(
        self, template_name: str, context: Dict[str, Any], output_path: str
    ) -> str:
        """
        Generate a Word document from a template with the provided context data.

        Args:
            template_name: Name of the template file (without path)
            context: Dictionary of data to populate the template
            output_path: Path where the generated document should be saved

        Returns:
            The path to the generated document
        """
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Load the template
        template_path = os.path.join(self.template_dir, template_name)

        # Log template information for debugging
        self.logger.debug(f"Loading template from: {template_path}")
        self.logger.debug(f"Template exists: {os.path.exists(template_path)}")

        if not os.path.exists(template_path):
            self.logger.error(f"Template not found at: {template_path}")
            self.logger.error(f"Current directory: {os.getcwd()}")
            self.logger.error(
                f"Template directory exists: {os.path.exists(self.template_dir)}"
            )
            if os.path.exists(self.template_dir):
                self.logger.error(
                    f"Files in template directory: {os.listdir(self.template_dir)}"
                )
            raise FileNotFoundError(f"Template not found: {template_path}")

        doc = DocxTemplate(template_path)

        # Render the template with the context data
        doc.render(context)

        # Save the document
        doc.save(output_path)
        self.logger.debug(f"Document saved to: {output_path}")

        return output_path
