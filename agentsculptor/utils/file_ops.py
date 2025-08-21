import os
import shutil
import ast
from agentsculptor.tools.dialog import DialogManager


def read_file(path: str) -> str:
    """Read a text file and return its contents."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {path}")
    except PermissionError:
        print(f"[ERROR] Permission denied: {path}")
    except Exception as e:
        print(f"[ERROR] Unexpected error reading {path}: {e}")
    return ""


def write_file(path: str, content: str, instruction: str = ""):
    """
    Write content to a file, creating directories if needed.
    If the file does not exist, ask the user for confirmation before creation.
    """
    try:
        if not os.path.exists(path):
            if not DialogManager.confirm_file_creation(path, instruction):
                print(f"[INFO] Skipping creation of {path}")
                return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"[ERROR] Failed to write to {path}: {e}")


def backup_file(path: str, suffix=".bak") -> str:
    """Rename a file to create a backup. Returns backup path."""
    try:
        if not os.path.exists(path):
            print(f"[ERROR] File not found: {path}")
            return ""
        backup_path = path + suffix
        shutil.copy2(path, backup_path)
        return backup_path
    except Exception as e:
        print(f"[ERROR] Failed to backup {path}: {e}")
        return ""


def move_file(src: str, dst: str, instruction: str = ""):
    """
    Move a file, creating directories if needed.
    Ask for confirmation if the destination file doesn't exist yet.
    """
    try:
        if not os.path.exists(dst):
            if not DialogManager.confirm_file_creation(dst, instruction):
                print(f"[INFO] Skipping move — destination {dst} not created.")
                return
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
    except Exception as e:
        print(f"[ERROR] Failed to move {src} to {dst}: {e}")


def delete_file(path: str):
    """Delete a file if it exists."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"[ERROR] Failed to delete {path}: {e}")


def modify_file(path: str, content: str, instruction: str = ""):
    """
    Modify (overwrite) an existing file's content, creating directories if needed.
    If the file does not exist, ask before creating it.
    """
    try:
        if not os.path.exists(path):
            if not DialogManager.confirm_file_creation(path, instruction):
                print(f"[INFO] Skipping modification — {path} not created.")
                return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"[ERROR] Failed to modify {path}: {e}")


def analyze_file(path: str) -> dict:
    """
    Analyze a Python file to identify logical sections:
    - Counts of functions and classes
    - List of top-level functions and classes with their line numbers

    Returns a dictionary summary.
    """
    content = read_file(path)
    if not content:
        return {}

    try:
        tree = ast.parse(content, filename=path)
    except SyntaxError as e:
        print(f"[ERROR] Syntax error while parsing {path}: {e}")
        return {}
    except Exception as e:
        print(f"[ERROR] Unexpected error analyzing {path}: {e}")
        return {}

    functions = []
    classes = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({"name": node.name, "lineno": node.lineno})
        elif isinstance(node, ast.ClassDef):
            classes.append({"name": node.name, "lineno": node.lineno})

    return {
        "path": path,
        "num_lines": content.count("\n") + 1,
        "num_functions": len(functions),
        "functions": functions,
        "num_classes": len(classes),
        "classes": classes,
    }
