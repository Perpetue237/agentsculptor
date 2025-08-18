# tools/refactor_code.py
import os
import re
from llm.client import VLLMClient


class RefactorCodeTool:
    def __init__(
        self,
        base_url: str = "http://localhost:8008",
        model: str = "openai/gpt-oss-120b"
    ):
        self.llm_client = VLLMClient(base_url=base_url, model=model)

    def _clean_code_content(self, content: str) -> str:
        """Strip markdown fences and whitespace from LLM output."""
        return re.sub(r"^```(?:python)?\n|```$", "", content.strip(), flags=re.MULTILINE).strip()

    def _detect_source_files(self, instruction: str) -> list:
        """Try to extract .py file names from the refactor instruction."""
        candidates = re.findall(r"(?:from|in|into)\s+([^\n]+?\.py)", instruction)
        files = []
        for cand in candidates:
            for part in re.split(r"\s*(?:,|and)\s*", cand.strip()):
                if part.endswith(".py"):
                    files.append(part.strip())
        seen = set()
        return [f for f in files if not (f in seen or seen.add(f))]

    def refactor_file(self, project_path: str, relative_path: str, instruction: str) -> None:
        """
        Load the latest version of the file(s) from disk and send to the LLM
        along with the refactoring instruction. Save the updated code back to disk.
        """
        full_path = os.path.join(project_path, relative_path)

        # Try to detect all relevant files mentioned in instruction; default to target file
        source_files = self._detect_source_files(instruction) or [relative_path]

        # Gather original + current code from disk
        original_parts = []
        current_parts = []
        for src in source_files:
            disk_path = os.path.join(project_path, src)
            if os.path.exists(disk_path):
                with open(disk_path, "r", encoding="utf-8") as f:
                    code = f.read()
                original_parts.append(f"# {src}\n{code}")
                current_parts.append(f"# {src}\n{code}")
            else:
                print(f"[WARN] Source file not found on disk: {src}")

        # Build LLM prompt
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a code refactoring assistant.\n"
                    "Given the original and current source code and a refactoring instruction, "
                    "return ONLY the updated source code for the target file.\n"
                    "Rules:\n"
                    "- Do not modify unrelated code.\n"
                    "- Preserve style and formatting.\n"
                    "- Use relative imports if needed.\n"
                    "- Return ONLY valid Python code — no comments, explanations, or markdown."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Original versions:\n```python\n{'\n\n'.join(original_parts)}\n```\n\n"
                    f"Current versions:\n```python\n{'\n\n'.join(current_parts)}\n```\n\n"
                    f"Refactoring instruction:\n{instruction}\n\n"
                    "Updated code:"
                )
            }
        ]

        # Send to LLM
        response = self.llm_client.chat(messages=messages, max_tokens=4096, temperature=0)

        # Clean and save the code
        cleaned_code = self._clean_code_content(response) or "# Empty file after refactor\n"
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(cleaned_code)

        print(f"[INFO] Refactored file {relative_path} according to instruction.")
