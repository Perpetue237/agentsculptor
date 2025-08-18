# tools/prepare_context.py
import os
from utils.file_ops import analyze_file  # We'll use your existing analyzer

def prepare_context(project_path: str, include_content=True, max_content_chars=10000):
    """
    Build a project context dictionary containing metadata for all files,
    optionally including the actual source content.

    Args:
        project_path (str): Root path of the project.
        include_content (bool): Whether to include file contents.
        max_content_chars (int): Truncate file content to this many characters.
    """
    context = {
        "files": {},
        "folders": []
    }

    for root, dirs, files in os.walk(project_path):
        rel_root = os.path.relpath(root, project_path)
        if rel_root == ".":
            rel_root = ""
        context["folders"].append(rel_root)

        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.join(rel_root, file) if rel_root else file
            file_info = {"size_bytes": os.path.getsize(file_path)}

            if file.endswith(".py"):
                try:
                    # Use the analyzer to get functions, classes, imports, etc.
                    analysis = analyze_file(file_path)
                except Exception as e:
                    print(f"[WARN] Could not analyze {rel_path}: {e}")
                    continue

                file_info.update({
                    "lines": analysis.get("num_lines", 0),
                    "functions": [
                        {"name": f["name"], "line": f["lineno"]}
                        for f in analysis.get("functions", [])
                    ],
                    "classes": [
                        {"name": c["name"], "line": c["lineno"]}
                        for c in analysis.get("classes", [])
                    ],
                    "imports": analysis.get("imports", [])
                })

                if include_content:
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            source = f.read()
                        file_info["content"] = source[:max_content_chars]
                    except UnicodeDecodeError:
                        print(f"[WARN] Could not read content of {rel_path} (non-UTF8).")

            else:
                # For non-Python files, store limited text content for certain types
                ext = os.path.splitext(file)[1]
                file_info["type"] = ext
                if include_content and ext in {".txt", ".md", ".json", ".yaml", ".yml"}:
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        file_info["content"] = content[:max_content_chars]
                    except UnicodeDecodeError:
                        print(f"[WARN] Could not read content of {rel_path} (non-UTF8).")

            context["files"][rel_path] = file_info

    return context
