# utils/file_ops.py
import os
import shutil
import ast

def read_file(path: str) -> str:
    """Read a text file and return its contents."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str):
    """Write content to a file, creating directories if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def backup_file(path: str, suffix=".bak") -> str:
    """Rename a file to create a backup. Returns backup path."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    backup_path = path + suffix
    shutil.copy2(path, backup_path)
    return backup_path


def move_file(src: str, dst: str):
    """Move a file, creating directories if needed."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)


def delete_file(path: str):
    """Delete a file if it exists."""
    if os.path.exists(path):
        os.remove(path)
        
def modify_file(path: str, content: str):
    """Modify (overwrite) an existing file's content, creating directories if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
def analyze_file(path: str) -> dict:
    """
    Analyze a Python file to identify logical sections:
    - Counts of functions and classes
    - List of top-level functions and classes with their line numbers
    
    Returns a dictionary summary.
    """
    content = read_file(path)
    
    try:
        tree = ast.parse(content, filename=path)
    except SyntaxError as e:
        print(f"[ERROR] Syntax error while parsing {path}: {e}")
        return {}

    functions = []
    classes = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({"name": node.name, "lineno": node.lineno})
        elif isinstance(node, ast.ClassDef):
            classes.append({"name": node.name, "lineno": node.lineno})

    summary = {
        "path": path,
        "num_lines": content.count("\n") + 1,
        "num_functions": len(functions),
        "functions": functions,
        "num_classes": len(classes),
        "classes": classes,
    }
    return summary


