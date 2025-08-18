TOOL_REGISTRY = [
    {
        "name": "backup_file",
        "description": "Backup a file before modification",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to backup"}
            },
            "required": ["path"]
        },
    },
    {
        "name": "create_file",
        "description": "Create a new file with content",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        },
    },
    {
        "name": "refactor_code",
        "description": "Refactor an existing file according to instructions",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "instruction": {"type": "string"}
            },
            "required": ["path", "instruction"]
        },
    },
    {
        "name": "update_imports",
        "description": "Update imports across files to use new module paths",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "instruction": {"type": "string"}
            },
            "required": ["path", "instruction"]
        },
    },
    {
        "name": "run_tests",
        "description": "Run the project test suite",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "format_code",
        "description": "Format code using Black",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        },
    }
]

TOOL_SIGNATURES = {
    "refactor_code": ["path", "instruction"],
    "update_imports": ["path", "instruction"],
    "create_file": ["path", "content"],
    "modify_file": ["path", "content"],
    "backup_file": ["path"],
    #"commit_changes": ["description"],
}

