# tools/refactor_code.py
import os
import re
from codesculptor.llm.client import VLLMClient
from codesculptor.llm.prompts import build_refactor_messages
from codesculptor.tools.dialog import DialogManager



class RefactorCodeTool:
    def __init__(self, base_url=None, model=None):
        # Read from environment if not explicitly passed
        self.base_url = (base_url or os.environ.get("VLLM_URL", "http://localhost:8008")).rstrip("/")
        self.model = model or os.environ.get("VLLM_MODEL", "openai/gpt-oss-120b")
        self.llm_client = VLLMClient(base_url=self.base_url, model=self.model)

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
    
    def _is_creation_required(self, instruction: str) -> bool:
        """
        Heuristic: If instruction suggests splitting, extracting,
        or moving code, treat creation as required.
        """
        keywords = ["split", "extract", "move", "create new file", "separate into"]
        return any(kw in instruction.lower() for kw in keywords)


    def refactor_file(self, project_path: str, relative_path: str, instruction: str) -> None:
        print(relative_path, instruction)
        """
        Load the latest version of the file(s) from disk and send to the LLM
        along with the refactoring instruction. Save the updated code back to disk.
        """
        full_path = os.path.join(project_path, relative_path)

        # 1. Detect candidate files
        source_files = self._detect_source_files(instruction) or [relative_path]

        # 2. Ask user to resolve ambiguity (new dialog step)
        source_files = DialogManager.choose_file(source_files, instruction)

        # 3. Confirm action before proceeding
        if not DialogManager.confirm_action(source_files, instruction):
            print("[INFO] Refactor cancelled by user.")
            return

        # 4. Gather original + current code from disk
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

        # 5. Build LLM prompt
        messages = build_refactor_messages(original_parts, current_parts, instruction)

        # 6. Send to LLM
        response = self.llm_client.chat(messages=messages, max_tokens=4096, temperature=0)

        # 7. Clean and prepare code
        cleaned_code = self._clean_code_content(response) or "# Empty file after refactor\n"

        # 8. Check if file exists or requires creation
        if not os.path.exists(full_path):
            # Ask user if we should create it
            if not DialogManager.confirm_file_creation(full_path, instruction):
                # Decide: skip vs fail depending on necessity
                if self._is_creation_required(instruction):
                    print(f"[ERROR] Cannot satisfy request — creation of {relative_path} is required.")
                    return
                else:
                    print(f"[INFO] Skipping creation of {relative_path} (not essential).")
                    return

        # 9. Write the updated file
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(cleaned_code)

        print(f"[INFO] Refactored file {relative_path} according to instruction.")
