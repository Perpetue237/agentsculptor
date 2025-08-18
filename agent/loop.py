# agent/loop.py
import os
import subprocess
from utils.file_ops import write_file, move_file, backup_file, modify_file, analyze_file
from tools.update_imports import update_imports
from tools.run_tests import run_tests
from tools.refactor_code import RefactorCodeTool

def make_tool_functions(project_path, context, refactor_tool, analysis_cache):
    return {
        "create_file": lambda path, content: write_file(os.path.join(project_path, path), content),

        #"modify_file": lambda path, content: modify_file(os.path.join(project_path, path), content),

        "backup_file": lambda path: (
            backup_file(os.path.join(project_path, path))
            if os.path.exists(os.path.join(project_path, path))
            else print(f"[WARN] File {path} not found — skipping backup.")
        ),

        #"move_file": lambda path, destination: move_file(project_path, path, destination),

        "update_imports": lambda path, instruction: update_imports(
            project_path, path, instruction, context=context
        ),

        "run_tests": lambda: run_tests(project_path),

        "format_code": lambda path=None: subprocess.run(["black", project_path], check=True),

        "refactor_code": lambda path, instruction: refactor_tool.refactor_file(
            project_path,
            path,
            instruction + (
                "\n\n[FILE STRUCTURE ANALYSIS]\n"
                f"Lines: {analysis_cache[path]['num_lines']}, "
                f"Functions: {analysis_cache[path]['num_functions']}, "
                f"Classes: {analysis_cache[path]['num_classes']}\n"
                "Functions:\n" + "\n".join(
                    f"- {f['name']} (line {f['lineno']})" for f in analysis_cache[path]["functions"]
                ) + "\n"
                "Classes:\n" + "\n".join(
                    f"- {c['name']} (line {c['lineno']})" for c in analysis_cache[path]["classes"]
                )
                if path in analysis_cache else ""
            )
        ),

        #"commit_changes": lambda description="Automated commit": (
           # subprocess.run(["git", "add", "."], cwd=project_path),
           # subprocess.run(["git", "commit", "-m", description], cwd=project_path)
        #),
    }

def dispatch_tool_call(tool_functions, step):
    tool = step["action"]
    args = {k: v for k, v in step.items() if k != "action"}
    func = tool_functions.get(tool)
    if not func:
        print(f"[WARN] Unknown action: {tool}")
        return
    try:
        func(**args)
        print(f"[INFO] Executed {tool} with args: {args}")
    except Exception as e:
        print(f"[ERROR] Failed to execute {tool}: {e}")

def run_loop(project_path, context, plan):
    refactor_tool = RefactorCodeTool()
    analysis_cache = {}  # You can populate this if needed
    tool_functions = make_tool_functions(project_path, context, refactor_tool, analysis_cache)

    for step in plan:
        dispatch_tool_call(tool_functions, step)

class AgentLoop:
    def __init__(self, planner, context, user_request, project_path):
        self.planner = planner
        self.context = context
        self.user_request = user_request
        self.project_path = project_path
        self.execution_log = []
        self.analysis_cache = {}
        self.refactor_tool = RefactorCodeTool()
        self.tool_functions = make_tool_functions(
            project_path=self.project_path,
            context=self.context,
            refactor_tool=self.refactor_tool,
            analysis_cache=self.analysis_cache
        )

    def dispatch_tool_call(self, call):
        tool = call["tool"]
        args = call.get("args", {})
        func = self.tool_functions.get(tool)
        if not func:
            return {"tool": tool, "status": "error", "error": "Unknown tool"}
        try:
            func(**args)
            return {"tool": tool, "status": "success", "args": args}
        except Exception as e:
            return {"tool": tool, "status": "error", "args": args, "error": str(e)}

    def run(self, max_iterations=3):
        for _ in range(max_iterations):
            plan = self.planner.generate_tool_calls(
                context=self.context,
                user_request=self.user_request,
                execution_log=self.execution_log
            )
            for call in plan:
                result = self.dispatch_tool_call(call)
                self.execution_log.append(result)
                print(f"[{result['status'].upper()}] {result['tool']} → {result.get('error', '')}")
