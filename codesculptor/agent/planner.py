# agent/planner.py
import json
from typing import Any, Dict, List, Optional
from codesculptor.llm.client import VLLMClient
from codesculptor.tools.registry import TOOL_REGISTRY, TOOL_SIGNATURES
import os

def format_tool_list(tool_registry: List[Dict]) -> str:
    return "\n".join(
        f"- '{tool['name']}': {tool['description']}" for tool in tool_registry
    )
    
def summarize_context(context: Dict[str, Any], max_files: int = 20, max_chars_per_file: int = 2000) -> str:
    lines = []
    files = context.get("files", {})
    folders = context.get("folders", [])

    lines.append("Folders:")
    for f in folders[:50]:
        lines.append(f"  - {f}")

    lines.append("\nFiles (top entries):")

    def sort_key(item):
        info = item[1]
        return info.get("lines", 0)

    for rel_path, info in sorted(files.items(), key=sort_key, reverse=True)[:max_files]:
        parts = [f"- {rel_path}"]
        if "lines" in info:
            parts.append(f"lines={info['lines']}")
        if "functions" in info:
            parts.append(f"funcs={info['functions']}")
        if "classes" in info:
            parts.append(f"classes={info['classes']}")
        if "imports" in info:
            imports = info.get("imports") or []
            if imports:
                parts.append("imports=" + ",".join(imports[:5]))
        lines.append("  " + " ".join(parts))

        content = info.get("content")
        if content:
            truncated = content[:max_chars_per_file]
            if rel_path.endswith(".py"):
                lines.append(f"  --- BEGIN FILE CONTENT ({rel_path}) ---")
                lines.append("```python")
                lines.append(truncated)
                lines.append("```")
                lines.append(f"  --- END FILE CONTENT ({rel_path}) ---")
            else:
                lines.append(f"  --- BEGIN FILE CONTENT ({rel_path}) ---")
                lines.append(truncated)
                lines.append(f"  --- END FILE CONTENT ({rel_path}) ---")

    dep_graph = context.get("dependency_graph")
    if dep_graph:
        lines.append("\nDependency graph (partial):")
        for k, deps in list(dep_graph.items())[:50]:
            lines.append(f"  - {k} -> {deps[:5]}")

    return "\n".join(lines)


def summarize_context_without_content(context: Dict[str, Any]) -> Dict[str, Any]:
    light_context = dict(context)
    light_files = {}
    for path, info in context.get("files", {}).items():
        light_files[path] = {k: v for k, v in info.items() if k != "content"}
    light_context["files"] = light_files
    return light_context


def _extract_json_from_text(text: str) -> Optional[str]:
    text = text.strip()
    try:
        json.loads(text)
        return text
    except Exception:
        pass

    open_idx = None
    for i, ch in enumerate(text):
        if ch in ("{", "["):
            open_idx = i
            open_ch = ch
            break
    if open_idx is None:
        return None

    close_ch = "}" if open_ch == "{" else "]"

    depth = 0
    for i in range(open_idx, len(text)):
        if text[i] == open_ch:
            depth += 1
        elif text[i] == close_ch:
            depth -= 1
            if depth == 0:
                candidate = text[open_idx: i + 1]
                try:
                    json.loads(candidate)
                    return candidate
                except Exception:
                    continue
    return None

class PlannerAgent:
    def __init__(self, base_url=None, model=None):
        # Read from environment if not explicitly passed
        self.base_url = (base_url or os.environ.get("VLLM_URL", "http://localhost:8008")).rstrip("/")
        self.model = model or os.environ.get("VLLM_MODEL", "openai/gpt-oss-120b")
        self.client = VLLMClient(base_url=self.base_url, model=self.model)

    def generate_tool_calls(
        self,
        context: Dict[str, Any],
        user_request: str,
        execution_log: Optional[List[Dict]] = None,
        max_tokens: int = 10000,
        temperature: float = 0.0
    ) -> List[Dict]:
        tool_list = format_tool_list(TOOL_REGISTRY)
        system_prompt = (
                "You are a software agent that plans and invokes tools to modify codebases.\n"
                "Your job is to return a JSON array of tool calls. Each call must include:\n"
                "- 'tool': name of the tool\n"
                "- 'args': dictionary of arguments\n\n"
                f"Available tools:\n{tool_list}\n\n"
                "Rules:\n"
                "1. Only return valid JSON — no markdown or commentary.\n"
                "2. Do not invent tools not listed.\n"
                "3. Use only the context and execution history provided.\n"
                "4. When importing between files in the same folder, use direct imports like 'from cli import main'.\n"
                "   Do not use relative imports (e.g., 'from .cli import main') or package-style imports (e.g., 'from app.cli import main').\n"
                "   Assume the code will be run as a script from within the folder, not as a package.\n"
                f"5. Use the exact argument names expected by each tool. Here are the expected argument names for each tool: {TOOL_SIGNATURES}. Please match them exactly.\n"
                "6. Crutial: \n"
                    "- If the file was provided in the original context, always first create a testing code in the same folder as te file to test (also here holds Do not use relative imports (e.g., 'from .cli import main') or package-style imports (e.g., 'from app.cli import main'), test it and back it up before modifying it! \n"
                    "- If the file was provided in the original context, run the test if provided. If not you can use actions from the tool registry to create a testing code in the same folder as the file to test. Choose a name prefixed by the name the file you want to write the test for. "
            )


        user_prompt = (
            f"PROJECT CONTEXT:\n{json.dumps(context, indent=2)}\n\n"
            f"USER REQUEST:\n{user_request}\n"
        )
        if execution_log:
            user_prompt += f"\nEXECUTION HISTORY:\n{json.dumps(execution_log, indent=2)}\n"

        response = self.client.chat(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        json_snippet = _extract_json_from_text(response)
        if not json_snippet:
            raise ValueError(f"No JSON could be extracted:\n{response}")
        return json.loads(json_snippet)