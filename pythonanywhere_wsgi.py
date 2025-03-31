import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Add the project directory to the path
project_home = "/home/abraaar07/mysite"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Log environment information
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python version: {sys.version}")
logger.info(f"Python path: {sys.path}")

# Check if templates directory exists
templates_dir = os.path.join(project_home, "templates")
word_dir = os.path.join(templates_dir, "word")

logger.info(f"Templates directory exists: {os.path.exists(templates_dir)}")
if os.path.exists(templates_dir):
    logger.info(f"Templates directory contents: {os.listdir(templates_dir)}")

    logger.info(f"Word directory exists: {os.path.exists(word_dir)}")
    if os.path.exists(word_dir):
        logger.info(f"Word directory contents: {os.listdir(word_dir)}")

# Import the Flask app
try:
    from app import app as application

    logger.info("Successfully imported the Flask application")
except Exception as e:
    logger.exception(f"Error importing Flask application: {str(e)}")
    raise
