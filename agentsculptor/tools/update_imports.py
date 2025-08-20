# tools/update_imports.py
import os
import re
from agentsculptor.llm.client import VLLMClient
from agentsculptor.llm.prompts import build_import_messages


base_url = (None or os.environ.get("VLLM_URL", "http://localhost:8008")).rstrip("/")
model = None or os.environ.get("VLLM_MODEL", "openai/gpt-oss-120b")

llm_client = VLLMClient(base_url=base_url, model=model)


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
        updated_code = (
            "# [TODO] No import update instruction was provided.\n"
            "# Please update the imports manually if needed.\n\n"
            + original_code
        )
    else:
        # Build prompt for the LLM
        messages = build_import_messages(original_code, instruction, context)
        response = llm_client.chat(messages=messages, max_tokens=4096, temperature=0.0)


        updated_code = re.sub(
            r"^```(?:python)?\n|```$", "", response.strip(), flags=re.MULTILINE
        ).strip()

        if not updated_code:
            print("[WARN] LLM returned empty update for imports, falling back to original code.")
            updated_code = original_code

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(updated_code)

    print(f"[INFO] Updated imports in {relative_path}")
