# agent/executor.py
import os
import subprocess
from utils.file_ops import write_file, move_file, backup_file, modify_file, analyze_file
from tools.update_imports import update_imports
from tools.run_tests import run_tests
from tools.refactor_code import RefactorCodeTool
from tools.prepare_context import prepare_context
from llm.client import VLLMClient


class ExecutorAgent:
    def __init__(self, project_path: str, context: dict, llm_base_url="http://localhost:8008", llm_model="openai/gpt-oss-120b"):
        self.project_path = project_path
        self.llm_client = VLLMClient(base_url=llm_base_url, model=llm_model)
        self.context = context
        self.refactor_tool = RefactorCodeTool()
        self.analysis_cache = {}  # Store analyze_file results here

    def execute_plan(self, plan):
        # Prepare context once at start

        for step in plan:
            action = step["action"]

            if action == "create_file":
                write_file(os.path.join(self.project_path, step["path"]), step.get("content", ""))

            elif action == "modify_file":
                modify_file(os.path.join(self.project_path, step["path"]), step["content"])

            elif action == "backup_file":
                try:
                    full_path = os.path.join(self.project_path, step["path"])
                    backup_path = backup_file(full_path)
                    print(f"[INFO] Backed up {step['path']} to {backup_path}")
                except FileNotFoundError:
                    print(f"[WARN] File {step['path']} not found — skipping backup.")

            elif action == "move_file":
                move_file(self.project_path, step["path"], step["destination"])

            elif action == "update_imports":
                path = step.get("path")
                instruction = step.get("instruction", "")
                if path:
                    update_imports(self.project_path, path, instruction, context=self.context)
                else:
                    print(f"[WARN] 'update_imports' step missing 'path'.")

            elif action == "run_tests":
                run_tests(self.project_path)

            elif action == "format_code":
                subprocess.run(["black", self.project_path], check=True)

            elif action == "refactor_code":
                path = step.get("path")
                instruction = step.get("instruction", "")

                # Attach analysis info if available
                analysis_info = ""
                if path in self.analysis_cache:
                    a = self.analysis_cache[path]
                    analysis_info = (
                        "\n\n[FILE STRUCTURE ANALYSIS]\n"
                        f"Lines: {a['num_lines']}, Functions: {a['num_functions']}, Classes: {a['num_classes']}\n"
                        "Functions:\n" + "\n".join(f"- {f['name']} (line {f['lineno']})" for f in a["functions"]) + "\n"
                        "Classes:\n" + "\n".join(f"- {c['name']} (line {c['lineno']})" for c in a["classes"])
                    )

                if path and instruction:
                    self.refactor_tool.refactor_file(
                        self.project_path,
                        path,
                        instruction + analysis_info
                    )
                else:
                    print(f"[WARN] 'refactor_code' step missing 'path' or 'instruction'.")

            elif action == "commit_changes":
                subprocess.run(["git", "add", "."], cwd=self.project_path)
                subprocess.run(
                    ["git", "commit", "-m", step.get("description", "Automated commit")],
                    cwd=self.project_path
                )

            else:
                print(f"[WARN] Unknown action: {action}")
