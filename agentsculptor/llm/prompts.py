# llm/prompts.py

from agentsculptor.tools.registry import TOOL_REGISTRY, TOOL_SIGNATURES


def format_tool_list(tool_registry):
    """Format the tool registry into a readable list for prompts."""
    return "\n".join(
        f"- '{tool['name']}': {tool['description']}" for tool in tool_registry
    )


def planner_system_prompt() -> str:
    """Return the system prompt for the PlannerAgent."""
    tool_list = format_tool_list(TOOL_REGISTRY)
    return (
                "You are a software agent that plans and invokes tools to modify codebases.\n"
                "Your job is to return a JSON array of tool calls. Each call must include:\n"
                "- 'tool': name of the tool\n"
                "- 'args': dictionary of arguments\n\n"
                f"Available tools:\n{tool_list}\n\n"
                "If you cannot perform an action say so and give the reason. Never noturn an error or an empty answer.\n"
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
                    "- If the file was provided in the original context, run the test if provided. If not you can use actions from the tool registry to create a testing code in the same folder as the file to test. Choose a name prefixed by the name the file you want to write the test for."
            )
    
def refactor_system_prompt() -> str:
    """System prompt for the refactoring tool."""
    return (
        "You are a code refactoring assistant.\n"
        "Given the original and current source code and a refactoring instruction, "
        "return ONLY the updated source code for the target file.\n"
        "Rules:\n"
        "- Do not modify unrelated code.\n"
        "- Preserve style and formatting.\n"
        "- Use relative imports if needed.\n"
        "- Return ONLY valid code — no comments, explanations, or markdown."
        "- If you cannot perform an action say so and give the reason. Never noturn an error or an empty answer."
    )


def build_refactor_messages(original_parts: list[str], current_parts: list[str], instruction: str) -> list[dict]:
    """Construct the messages payload for the LLM refactor request."""
    return [
        {"role": "system", "content": refactor_system_prompt()},
        {
            "role": "user",
            "content": (
                f"Original versions:\n```python\n{'\n\n'.join(original_parts)}\n```\n\n"
                f"Current versions:\n```python\n{'\n\n'.join(current_parts)}\n```\n\n"
                f"Refactoring instruction:\n{instruction}\n\n"
                "Updated code:"
            ),
        },
    ]


def import_system_prompt() -> str:
    """System prompt for the import refactoring tool."""
    return (
        "You are a Python import statement refactoring assistant.\n"
        "You have access to a summary of the project structure and files.\n"
        "Your only task: rewrite ONLY the import statements according to the given instruction.\n"
        "Keep all other code exactly as-is.\n"
        "Return ONLY the full updated source code. Do NOT explain, comment, or add markdown."
    )


def build_import_messages(original_code: str, instruction: str, context: str | None = None) -> list[dict]:
    """Construct the messages payload for the import update request."""
    context_snippet = f"Project context (summary):\n{context or ''}\n"

    return [
        {"role": "system", "content": import_system_prompt()},
        {
            "role": "user",
            "content": (
                f"{context_snippet}\n"
                f"Original code:\n```python\n{original_code}\n```\n\n"
                f"Instruction:\n{instruction}\n\n"
                "Updated code:\n"
            ),
        },
    ]
