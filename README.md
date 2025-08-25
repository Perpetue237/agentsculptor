# agentsculptor

**agentsculptor** is an experimental AI-powered development agent designed to **analyze, refactor, and extend Python projects automatically**. 
It uses an OpenAI-like planner–executor loop on top of a [vLLM](https://github.com/vllm-project/vllm) backend, combining project context analysis, structured tool calls, and iterative refinement.

``` mermaid
flowchart TD
    %% === NODES ===
    A([💬 User Request])
    B([🧠 Planner Agent])
    C([🔁 Agent Loop])
    D{{🛠️ Tools}}

    %% Tools
    D1([🧪 Run Tests])       
    %% Stadium shape
    D2([📄 File Creation])
    D3([🖋️ Refactor Code])
    D4([🔗 Update Imports])
    D5([🎨 Format Code])
    D6[/💾 Backup/]          
    %% Parallelogram

    E([🏆 Success])

    %% === EDGES ===
    A --> B -->|Generates JSON Plan| C --> D
    D -.->|run_tests| D1
    D <-.->|create_file| D2
    D <-.->|refactor_code| D3
    D <-.->|update_imports| D4
    D <-.->|format_code| D5
    D -.->|backup_file| D6

    D1 -->|❌ Tests Fail| B
    D1 -->|✅ Tests Pass| E

    %% === STYLES (softer colors) ===
    style A fill:#BBDEFB,stroke:#64B5F6,color:#0D47A1
    style B fill:#E1BEE7,stroke:#BA68C8,color:#4A148C
    style C fill:#FFE0B2,stroke:#FFB74D,color:#E65100
    style D fill:#CFD8DC,stroke:#90A4AE,color:#263238

    %% Normal tools - soft blue
    style D2 fill:#B3E5FC,stroke:#4FC3F7,color:#01579B
    style D3 fill:#B3E5FC,stroke:#4FC3F7,color:#01579B
    style D4 fill:#B3E5FC,stroke:#4FC3F7,color:#01579B
    style D5 fill:#B3E5FC,stroke:#4FC3F7,color:#01579B

    %% Special tools
    style D1 fill:#C8E6C9,stroke:#81C784,color:#1B5E20   
    style D6 fill:#FFCCBC,stroke:#FF8A65,color:#BF360C   

    style E fill:#C5E1A5,stroke:#AED581,color:#33691E
```

## ⚠️ Disclaimer

AgentSculptor is an experimental project created for the OpenAI Open Model Hackathon.
It has only been tested with gpt-oss-120b via vLLM.

Other models may work, but compatibility is not guaranteed at this stage. Use at your own risk and please share feedback if you experiment with different setups.

---
## Table of Content
- [agentsculptor](#agentsculptor)
  - [⚠️ Disclaimer](#️-disclaimer)
  - [Table of Content](#table-of-content)
  - [🚀 Getting Started / Usage](#-getting-started--usage)
    - [1. Install from PyPI](#1-install-from-pypi)
    - [2. Or install from source](#2-or-install-from-source)
    - [3. Set environment variables](#3-set-environment-variables)
    - [4. Run CLI commands](#4-run-cli-commands)
    - [5. Other examples](#5-other-examples)
    - [6. Workflow Overview](#6-workflow-overview)
  - [🚀 Features](#-features)
  - [📦 Repository Structure](#-repository-structure)
  - [👨‍💻 Developer Guide](#-developer-guide)
    - [🟢 Option A — Development in VS Code DevContainer](#-option-a--development-in-vs-code-devcontainer)
      - [1. DevContainer](#1-devcontainer)
      - [2. Dockerfile](#2-dockerfile)
      - [3. Python Dependencies](#3-python-dependencies)
      - [4. Start](#4-start)
    - [🔵 Option B — Without DevContainer (Dedicated virtual environment)](#-option-b--without-devcontainer-dedicated-virtual-environment)
  - [Workflow](#workflow)
    - [🛠️ Tools Available](#️-tools-available)
    - [💡 Usage Notes](#-usage-notes)
    - [⚙️ How It Works](#️-how-it-works)
      - [📋 Planner Agent (Reasoning Layer)](#-planner-agent-reasoning-layer)
      - [🔁 Agent Loop (Execution Layer)](#-agent-loop-execution-layer)
      - [🛠️ Tools (Action Layer)](#️-tools-action-layer)
      - [♻️ Re-Planning \& Self-Healing (Future)](#️-re-planning--self-healing-future)
  - [🚀 Roadmap](#-roadmap)
  - [🤝 Contributions](#-contributions)
    - [1. 🛠️ Setup Your Environment](#1-️-setup-your-environment)
    - [2. 🔧 Make Your Changes](#2--make-your-changes)
    - [3. 🧪 Test Your Changes](#3--test-your-changes)
    - [4. 📦 Commit \& Submit](#4--commit--submit)
    - [5. ⚡ Code Review](#5--code-review)
    - [6. 🎉 Celebrate!](#6--celebrate)
  - [📄 License](#-license)


---

## 🚀 Getting Started / Usage

Python 3.12 or higher is required. Follow these steps to install and use **agentsculptor**:

### 1. Install from PyPI

```bash
pip install agentsculptor
```

### 2. Or install from source

Clone the repository and install in editable mode (for local changes):

```bash
git clone https://github.com/Perpetue237/agentsculptor.git
cd agentsculptor
pip install -e .
```

### 3. Set environment variables

agentsculptor requires a running vLLM server. Set:

```bash
export VLLM_URL="http://localhost:8008"
export VLLM_MODEL="openai/gpt-oss-120b"
```

Adjust according to your server setup.

### 4. Run CLI commands

Generate or refactor code with `agentsculptor-cli`. For example, to create a basic Dockerized FastAPI app:

```bash
agentsculptor-cli ./test_project "create files for a basic dockerized FastAPI application. The initial app should just return a JSON with 'hello to the OpenAI community'"
```

This will:

* Generate a minimal FastAPI app structure.
* Create Dockerfiles for containerization.
* Initialize the project in `./test_project`.

### 5. Other examples

```bash
agentsculptor-cli ./test_project "create fast api app with clear instructions on how to run it."
  ```

```bash
agentsculptor-cli ./test_project "Merge multiple Python modules into a single file."
  ```

```bash
agentsculptor-cli ./test_project "Refactor functions and automatically generate unit tests."
  ```

```bash
agentsculptor-cli ./test_project "Refactor my codebase and modernize. Update imports across the project after refactoring."
  ```

### 6. Workflow Overview

1. `prepare_context` scans your project.
2. `PlannerAgent` outputs a structured JSON plan.
3. `AgentLoop` executes each tool step by step.
4. Tests are run automatically (existing or generated).
5. Changes are applied safely, with backups if needed.


## 🚀 Features

* 📂 **Project Context Builder** – Parses files, functions, classes, and imports.
* 🧠 **Planner Agent** – Generates structured JSON plans of tool calls (no free-form text).
* 🔁 **Agent Loop** – Executes tool calls, tracks logs, and retries if needed.
* 🛠️ **Tool Registry** – Includes file creation, backup, import updates, code refactoring, and test execution.
* 🧪 **Automated Testing** – Runs `pytest` or generated test files before/after modifications.
* 🖋️ **Code Refactoring** – Uses LLM guidance with file structure hints for safer transformations.

---

## 📦 Repository Structure

```
.
|-- LICENSE                      # Open-source license file (MIT, Apache, etc.)
|-- README.md                    # Project documentation / usage instructions
|-- agentsculptor/                # Main Python package
|   |-- __init__.py              # Marks this as a Python package
|   |-- __pycache__/             # Auto-generated bytecode cache
|   |-- agent/                   # Agent logic (planner, executor, loop, etc.)
|   |-- llm/                     # LLM client + prompt handling
|   |-- main.py                  # CLI or entrypoint for running agentsculptor
|   |-- tools/                   # Helper modules (refactor_code, run_tests, etc.)
|   `-- utils/                   # Utility functions (file ops, logging, search, etc.)
|-- agentsculptor.egg-info/       # Metadata for packaging (setuptools)
|   |-- PKG-INFO                 # Package metadata (name, version, summary)
|   |-- SOURCES.txt              # List of source files included in the distribution
|   |-- dependency_links.txt     # Deprecated mechanism for dependency links
|   |-- entry_points.txt         # Console_scripts / plugin entry points
|   |-- requires.txt             # Runtime dependencies for installation
|   `-- top_level.txt            # Top-level package(s) exposed (here: "agentsculptor")
|-- setup.py                     # Build/install configuration for setuptools
|-- test_project/                # Example project used for testing/refactoring
|   |-- Dockerfile               # Docker container config for test project
|   |-- main.py                  # Example application entrypoint
|   |-- requirements.txt         # Test project dependencies
|   `-- test_main.py             # Unit tests for test project
`-- tests/                       # Tests for agentsculptor itself (not the example project)
```

---

## 👨‍💻 Developer Guide

This repository supports development using VS Code DevContainers.

> **Note**: The vLLM server is run separately. Make sure it is running at VLLM_URL and serving VLLM_MODEL. See /vllm-server-config/README.md for instructions on running the vLLM server.

### 🟢 Option A — Development in VS Code DevContainer

This repository provides a `.devcontainer` folder for an optimized development environment with docker.

#### 1. DevContainer

Create `.devcontainer/devcontainer.json`:
  ```json
  {
      "name": "agentsculptor",
      "build": {
        "dockerfile": "Dockerfile"
      },
      "features": {},
      "containerEnv": {
        "PYTHONUNBUFFERED": "1"
      },
      "customizations": {
        "vscode": {
          "extensions": [
              "ms-python.python",
              "ms-toolsai.jupyter",
              "innerlee.nvidia-smi",
              "Leonardo16.nvidia-gpu",
              "RSIP-Vision.nvidia-smi-plus",
              "yzhang.markdown-all-in-one",
              "MermaidChart.vscode-mermaid-chart",
              "Gruntfuggly.mermaid-export"
          ]
        }
      }
    }
  ```

#### 2. Dockerfile

`.devcontainer/Dockerfile`:
  ```bash
  FROM python:3.12-slim

  ENV DEBIAN_FRONTEND=noninteractive
  ENV TZ=Europe/Berlin

  COPY . .

  RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*
  RUN pip3 install --no-cache-dir -r requirements.txt
  ```

#### 3. Python Dependencies

`requirements.txt`:
  ```
  black
  pytest
  commitizen
  requests
  ```

#### 4. Start

1. Open the project in VS Code.

2. Click Reopen in Container.

3. Make sure the vLLM server is running and the environment variables are set:
    ```bash
    export VLLM_URL=http://localhost:8008
    
    ```
4. Intall agentsculptor
    ```bash
    pip install -e .
    ```

now you can use the `agentsculptor-cl`.

### 🔵 Option B — Without DevContainer (Dedicated virtual environment)


---
## Workflow

1. `prepare_context` scans your project files.
2. `PlannerAgent` generates a JSON plan of tool calls.
3. `AgentLoop` executes each tool in sequence.
4. Tests run (if available or auto-generated).
5. Changes are applied safely (backup first).

---
### 🛠️ Tools Available

Each tool in **agentsculptor** has a **name, description, and parameters**. You can use these tools via the CLI or programmatically.

| Tool | Description | Parameters | Example Usage |
|------|-------------|------------|---------------|
| **💾 `backup_file`** | Backup a file before modification to ensure safety. | `path` (string) → File path to backup | `{"path": "app/main.py"}` |
| **📄 `create_file`** | Create a new file with content. | `path` (string), `content` (string) → File path and initial content | `{"path": "app/utils.py", "content": "def helper(): pass"}` |
| **🖋️ `refactor_code`** | Refactor an existing file according to instructions. | `path` (string), `instruction` (string) → File to refactor and the transformation instruction | `{"path": "app/main.py", "instruction": "Extract helper functions from main()"}` |
| **🔗 `update_imports`** | Update imports across files to use new module paths. | `path` (string), `instruction` (string) → File or folder to scan/update and guidance | `{"path": "app/", "instruction": "Replace old module imports with mathlib.py"}` |
| **🧪 `run_tests`** | Run the project test suite to ensure changes are safe. | None | `{"path": ""}` |
| **🎨 `format_code`** | Format code using Black to maintain consistent style. | `path` (string) → File or directory to format | `{"path": "app/"}` |

### 💡 Usage Notes

- **Order matters**: Typically, `backup_file` runs before `refactor_code` or `update_imports`.  
- **Chaining tools**: You can combine `create_file`, `refactor_code`, and `update_imports` in a single workflow.  
- **Tests & safety**: Run `run_tests` after code modifications to catch issues automatically.  
- **Formatting**: `format_code` can be applied at the end of the workflow for clean, readable code.  


---

### ⚙️ How It Works

The agentsculptor agent runs on an OpenAI-like planner–executor loop, designed to make structured, safe, and iterative changes to your codebase.

``` mermaid
flowchart TD
    %% === NODES ===
    A([💬 User Request])
    B([🧠 Planner Agent])
    C([🔁 Agent Loop])
    D{{🛠️ Tools}}

    %% Tools
    D1([🧪 Run Tests])       
    %% Stadium shape
    D2([📄 File Creation])
    D3([🖋️ Refactor Code])
    D4([🔗 Update Imports])
    D5([🎨 Format Code])
    D6[/💾 Backup/]          
    %% Parallelogram

    E([🏆 Success])

    %% === EDGES ===
    A --> B -->|Generates JSON Plan| C --> D
    D -->|run_tests| D1
    D <-->|create_file| D2
    D <-->|refactor_code| D3
    D <-->|update_imports| D4
    D <-->|format_code| D5
    D -->|backup_file| D6

    D1 -->|❌ Tests Fail| B
    D1 -->|✅ Tests Pass| E

    %% === STYLES (softer colors) ===
    style A fill:#BBDEFB,stroke:#64B5F6,color:#0D47A1
    style B fill:#E1BEE7,stroke:#BA68C8,color:#4A148C
    style C fill:#FFE0B2,stroke:#FFB74D,color:#E65100
    style D fill:#CFD8DC,stroke:#90A4AE,color:#263238

    %% Normal tools - soft blue
    style D2 fill:#B3E5FC,stroke:#4FC3F7,color:#01579B
    style D3 fill:#B3E5FC,stroke:#4FC3F7,color:#01579B
    style D4 fill:#B3E5FC,stroke:#4FC3F7,color:#01579B
    style D5 fill:#B3E5FC,stroke:#4FC3F7,color:#01579B

    %% Special tools
    style D1 fill:#C8E6C9,stroke:#81C784,color:#1B5E20   
    style D6 fill:#FFCCBC,stroke:#FF8A65,color:#BF360C   

    style E fill:#C5E1A5,stroke:#AED581,color:#33691E
```

#### 📋 Planner Agent (Reasoning Layer)

Takes your natural language request (e.g., “merge utils.py and helpers.py into one module”).

Uses the project context (functions, classes, imports) to understand the current codebase.

Produces a structured JSON plan of tool calls – never free text.
Example:

```json
{
  "action": "refactor_code",
  "args": {
    "path": "utils/helpers.py",
    "instruction": "merge into utils.py"
  }
}
```

#### 🔁 Agent Loop (Execution Layer)

Iterates through the planned tool calls one by one.

Ensures dependencies are respected (e.g., backup → refactor → update imports → run tests).

Captures logs and errors for each step, with the ability to retry.

#### 🛠️ Tools (Action Layer)

The agent never edits files directly. Instead, it calls specialized tools:

backup_file → snapshot before modifying.

create_file → safely generate new files.

refactor_code → apply structured code transformations.

update_imports → keep imports consistent.

run_tests → verify changes with pytest.

format_code → ensure style consistency with black.

This makes the workflow transparent, reproducible, and debuggable.

#### ♻️ Re-Planning & Self-Healing (Future)

If a step fails (e.g., tests break), the agent will be able to re-plan automatically.

The loop can feed test results or error logs back into the Planner Agent, generating a new plan until success.

This section emphasizes the structured loop, safety-first approach, and extensibility of your agent.

---

## 🚀 Roadmap  

Here’s what’s next for **AgentSculptor**:  

- [ ] **Vector store DB integration** → persistent context & memory across sessions  
- [ ] **More refactoring tools** → auto-docstring generation, linting, style normalization  
- [ ] **Framework templates** → easy scaffolding for Flask, Django, Streamlit, etc.  
- [ ] **Interactive mode** → iterative refinement with conversational feedback  
- [ ] **Multi-agent workflows** → planner + executor agents collaborating on complex tasks  
- [ ] **VS Code extension** → invoke AgentSculptor directly from your editor  



## 🤝 Contributions

We welcome contributions of all types—bug fixes, feature enhancements, documentation improvements, or new tools. Here's how you can help:

### 1. 🛠️ Setup Your Environment
Clone the repository and install in editable mode:

```bash
git clone https://github.com/Perpetue237/agentsculptor.git
cd agentsculptor
pip install -e .
```
Set up required environment variables:

```bash
export VLLM_URL="http://localhost:8008"
export VLLM_MODEL="openai/gpt-oss-120b"
```

### 2. 🔧 Make Your Changes
* **Add features**: Create new tools or improve the agent workflow.

* **Refactor code**: Improve readability, structure, or performance.

* **Fix bugs**: Check the issues list and pick tasks you can solve.

* **Update documentation**: Keep README, comments, and examples up to date.

### 3. 🧪 Test Your Changes
Run the automated test suite or add your own:

```bash
pytest
``` 
### 4. 📦 Commit & Submit
* Use clear, descriptive commit messages.

* Push your branch and open a Pull Request (PR).

* Include a description of your change and reference related issues.

### 5. ⚡ Code Review
All contributions go through review for quality and safety. Be ready to iterate on feedback.

### 6. 🎉 Celebrate!
Once approved and merged, your contribution becomes part of agentsculptor!

---

## 📄 License

Apache License. See [LICENSE](LICENSE) for details.
