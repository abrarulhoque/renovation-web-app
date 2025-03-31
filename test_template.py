import os
import logging
import sys
from services.document_generation.template_modifier import modify_template

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def test_template_generation():
    """Test the template generation process"""
    try:
        # Get the base directory (project root)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"Base directory: {base_dir}")

        # Check if templates directory exists
        templates_dir = os.path.join(base_dir, "templates")
        logger.info(f"Templates directory exists: {os.path.exists(templates_dir)}")

        if os.path.exists(templates_dir):
            logger.info(f"Templates directory contents: {os.listdir(templates_dir)}")

            # Check if word directory exists
            word_dir = os.path.join(templates_dir, "word")
            logger.info(f"Word directory exists: {os.path.exists(word_dir)}")

            if os.path.exists(word_dir):
                logger.info(f"Word directory contents: {os.listdir(word_dir)}")

                # Check if original template exists
                original_template = os.path.join(word_dir, "renovation_quote.docx")
                logger.info(
                    f"Original template exists: {os.path.exists(original_template)}"
                )

                if os.path.exists(original_template):
                    # Try to modify the template
                    logger.info("Attempting to modify template...")
                    new_template = modify_template(base_dir=base_dir)
                    logger.info(f"Template modified successfully: {new_template}")
                    logger.info(f"New template exists: {os.path.exists(new_template)}")
                else:
                    logger.error("Original template does not exist!")
            else:
                logger.error("Word directory does not exist!")
        else:
            logger.error("Templates directory does not exist!")

    except Exception as e:
        logger.exception(f"Error testing template generation: {str(e)}")


if __name__ == "__main__":
    test_template_generation()
