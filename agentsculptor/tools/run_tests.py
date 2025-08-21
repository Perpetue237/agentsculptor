# tools/run_tests.py
import subprocess
from agentsculptor.utils.logging import setup_logging, get_logger

setup_logging("DEBUG")
logger = get_logger()

def run_tests(project_path: str):
    """
    Run the test suite in the project directory using pytest.
    """
    logger.info("[INFO] Running tests...")
    try:
        result = subprocess.run(
            ["pytest", "--maxfail=1", "--disable-warnings", "-q"],
            cwd=project_path,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        if result.returncode == 0:
            logger.info("[INFO] Tests passed successfully.")
        else:
            logger.error("[ERROR] Tests failed.")
            print(result.stderr)
    except FileNotFoundError:
        logger.error("[ERROR] pytest is not installed or not found in PATH.")
