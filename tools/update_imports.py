# tools/update_imports.py
import os
import re
from llm.client import VLLMClient

llm_client = VLLMClient(base_url="http://localhost:8008", model="openai/gpt-oss-120b")


def update_imports(project_path: str, relative_path: str, instruction: str = None, context: str = None):
    """
    Update Python import statements in a file or folder using an LLM,
    with access to relevant project context (passed in by the caller).
    """
    full_path = os.path.join(project_path, relative_path)

    if not os.path.exists(full_path):
        print(f"[WARN] Path {relative_path} not found for import update.")
        return

    # Folder mode — process recursively
    if os.path.isdir(full_path):
        for root, _, files in os.walk(full_path):
            for file in files:
                if file.endswith(".py"):
                    rel_file_path = os.path.relpath(os.path.join(root, file), project_path)
                    update_imports(project_path, rel_file_path, instruction, context=context)
        return

    with open(full_path, "r", encoding="utf-8") as f:
        original_code = f.read()

    if not instruction:
        # Simple regex fallback when no LLM instruction is provided
        replacements = {
            r"from\s+main\s+import": "from app.api import",
            r"import\s+main": "import app.api",
        }
        updated_code = original_code
        for pattern, replacement in replacements.items():
            updated_code = re.sub(pattern, replacement, updated_code)
    else:
        # Build prompt for the LLM
        system_prompt = (
            "You are a Python import statement refactoring assistant.\n"
            "You have access to a summary of the project structure and files.\n"
            "Your only task: rewrite ONLY the import statements according to the given instruction.\n"
            "Keep all other code exactly as-is.\n"
            "Return ONLY the full updated source code. Do NOT explain, comment, or add markdown."
        )

        context_snippet = f"Project context (summary):\n{context or ''}\n"

        user_prompt = (
            f"{context_snippet}\n"
            f"Original code:\n```python\n{original_code}\n```\n\n"
            f"Instruction:\n{instruction}\n\n"
            "Updated code:\n"
        )

        response = llm_client.chat(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=4096,
            temperature=0.0,
        )

        updated_code = re.sub(
            r"^```(?:python)?\n|```$", "", response.strip(), flags=re.MULTILINE
        ).strip()

        if not updated_code:
            print("[WARN] LLM returned empty update for imports, falling back to original code.")
            updated_code = original_code

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(updated_code)

    print(f"[INFO] Updated imports in {relative_path}")
