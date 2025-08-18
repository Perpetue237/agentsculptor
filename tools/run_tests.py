# tools/run_tests.py
import subprocess

def run_tests(project_path: str):
    """
    Run the test suite in the project directory using pytest.
    """
    print("[INFO] Running tests...")
    try:
        result = subprocess.run(
            ["pytest", "--maxfail=1", "--disable-warnings", "-q"],
            cwd=project_path,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        if result.returncode == 0:
            print("[INFO] Tests passed successfully.")
        else:
            print("[ERROR] Tests failed.")
            print(result.stderr)
    except FileNotFoundError:
        print("[ERROR] pytest is not installed or not found in PATH.")
