# agent/loop.py
import os
import sys
import subprocess
from agentsculptor.utils.file_ops import write_file, backup_file
from agentsculptor.tools.update_imports import update_imports
from agentsculptor.tools.run_tests import run_tests
from agentsculptor.tools.refactor_code import RefactorCodeTool
from agentsculptor.utils.logging import setup_logging, get_logger

setup_logging(level="DEBUG")
logger = get_logger()


def safe_tool(func):
    """Decorator to make any tool return structured results with error handling."""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    return wrapper


def make_tool_functions(project_path, context, refactor_tool, analysis_cache):
    return {
        "create_file": safe_tool(
            lambda path, content: write_file(os.path.join(project_path, path), content)
        ),

        "backup_file": safe_tool(
            lambda path: backup_file(os.path.join(project_path, path))
        ),

        "update_imports": safe_tool(
            lambda path, instruction: update_imports(project_path, path, instruction, context=context)
        ),

        "run_tests": safe_tool(
            lambda: run_tests(project_path)
        ),

        "format_code": safe_tool(
            lambda path=None: subprocess.run(["black", project_path], check=True)
        ),

        "refactor_code": safe_tool(
            lambda path, instruction: refactor_tool.refactor_file(
                project_path,
                path,
                instruction + (
                    "\n\n[FILE STRUCTURE ANALYSIS]\n"
                    f"Lines: {analysis_cache.get(path, {}).get('num_lines', 0)}, "
                    f"Functions: {analysis_cache.get(path, {}).get('num_functions', 0)}, "
                    f"Classes: {analysis_cache.get(path, {}).get('num_classes', 0)}\n"
                )
            )
        ),
    }


def dispatch_tool_call(tool_functions, step):
    tool = step.get("action") or step.get("tool")
    args = step.get("args", {}) 

    if tool == "noop":
        return {"tool": "noop", "status": "noop", "args": args, "result": args.get("reason", "No-op")}
    func = tool_functions.get(tool)

    if not func:
        return {"tool": tool, "status": "error", "args": args, "error": "Unknown tool"}

    result = func(**args)
    return {"tool": tool, **result, "args": args}


def run_loop(project_path, context, plan):
    refactor_tool = RefactorCodeTool()
    analysis_cache = {}
    tool_functions = make_tool_functions(project_path, context, refactor_tool, analysis_cache)

    for step in plan:
        result = dispatch_tool_call(tool_functions, step)
        status = result["status"].upper()
        print(f"[{status}] {result['tool']} → {result.get('error', '') or 'ok'}")


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
            analysis_cache=self.analysis_cache,
        )

    def dispatch_tool_call(self, call):
        result = dispatch_tool_call(self.tool_functions, call)
        self.execution_log.append(result)
        return result

    def run(self, max_iterations=3):
        for iteration in range(max_iterations):
            logger.iteration(iteration+1, "Planning...")

            try:
                plan = self.planner.generate_tool_calls(
                    context=self.context,
                    user_request=self.user_request,
                    execution_log=self.execution_log,
                )
            except RuntimeError as e:
                logger.fatal(f"Could not generate plan: {e}")
                print("Please check that vLLM is running and reachable at your VLLM_URL.")
                sys.exit(1)

            if not plan:
                logger.stop("Planner returned no further actions. Exiting early.")
                break

            all_success = True
            for call in plan:
                tool = call.get("tool")
                args = call.get("args", {})

                if tool == "noop":
                    logger.noop(f"{args.get('reason', 'Planner decided no action is possible.')}")
                    # stop iterating further
                    return
                result = self.dispatch_tool_call(call)
                status = result["status"].upper()
                print(f"[{status}] {result['tool']} → {result.get('error', '') or 'ok'}")
                if result["status"] != "success":
                    all_success = False

            if all_success:
                logger.stop("All actions succeeded, stopping early.")
                break
