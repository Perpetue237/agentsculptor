# CodeSculptor

**CodeSculptor** is an experimental AI-powered development agent designed to **analyze, refactor, and extend Python projects automatically**.
It uses an OpenAI-like planner–executor loop on top of a [vLLM](https://github.com/vllm-project/vllm) backend, combining project context analysis, structured tool calls, and iterative refinement.

---
## Table of Content
- [CodeSculptor](#codesculptor)
  - [Table of Content](#table-of-content)
  - [🚀 Getting Started / Usage](#-getting-started--usage)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Install the package](#2-install-the-package)
    - [3. Set environment variables](#3-set-environment-variables)
    - [4. Run CLI commands](#4-run-cli-commands)
    - [5. Other examples](#5-other-examples)
    - [6. Workflow Overview](#6-workflow-overview)
  - [🚀 Features](#-features)
  - [📦 Repository Structure](#-repository-structure)
  - [⚡ Quick Setup with DevContainer](#-quick-setup-with-devcontainer)
    - [1. DevContainer](#1-devcontainer)
    - [2. Dockerfile](#2-dockerfile)
    - [3. Python Dependencies](#3-python-dependencies)
    - [4. Start the DevContainer](#4-start-the-devcontainer)
    - [5. Using the Agent](#5-using-the-agent)
  - [⚡ Usage](#-usage)
    - [Workflow](#workflow)
  - [🛠️ Tools Available](#️-tools-available)
  - [👨‍💻 Coding](#-coding)
    - [Development Setup](#development-setup)
    - [How It Works](#how-it-works)
  - [🌍 Roadmap](#-roadmap)
  - [📄 License](#-license)


---

## 🚀 Getting Started / Usage

Follow these steps to install and use **CodeSculptor**:

### 1. Clone the repository

```bash
git clone https://github.com/Perpetue237/codesculptor.git
cd codesculptor
```

### 2. Install the package

Use editable mode to allow local changes:

```bash
pip install -e .
```

### 3. Set environment variables

CodeSculptor requires a running vLLM server. Set:

```bash
export VLLM_URL="http://localhost:8008"
export VLLM_MODEL="openai/gpt-oss-120b"
```

Adjust according to your server setup.

### 4. Run CLI commands

Generate or refactor code with `codesculptor-cli`. For example, to create a basic Dockerized FastAPI app:

```bash
codesculptor-cli ./test_project "create files for a basic dockerized FastAPI application. The initial app should just return a JSON with 'hello to the OpenAI community'"
```

This will:

* Generate a minimal FastAPI app structure.
* Create Dockerfiles for containerization.
* Initialize the project in `./test_project`.

### 5. Other examples

* Merge multiple Python modules into a single file.
* Refactor functions and automatically generate unit tests.
* Update imports across the project after refactoring.

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
├── main.py                # CLI entrypoint
├── agent/                 # Core agent logic
│   ├── planner.py         # PlannerAgent → generates tool calls
│   ├── loop.py            # AgentLoop → executes plans
│   └── executor.py        # (reserved for future execution abstraction)
├── llm/                   # vLLM client and prompts
│   ├── client.py
│   └── prompts.py
├── tools/                 # Actionable tools
│   ├── prepare_context.py # Builds project context
│   ├── refactor_code.py
│   ├── run_tests.py
│   ├── update_imports.py
│   └── registry.py
├── utils/                 # Utilities
│   ├── file_ops.py
│   ├── logging.py
│   └── search.py
├── test_project/           # Dockerized test project
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/main.py
└── tests/                  # Reserved for unit/integration tests
```

---

## ⚡ Quick Setup with DevContainer

This repository provides a **VS Code DevContainer** for an optimized development environment with GPU support and vLLM.

### 1. DevContainer

Create `.devcontainer/devcontainer.json`:

```json
{
  "name": "gpt-oss-120b-vllm",
  "build": {
    "dockerfile": "Dockerfile"
  },
  "runArgs": [
    "--gpus", "\"device=5,6\"",
    "--shm-size=64gb",
    "--ulimit", "memlock=-1",
    "--ulimit", "stack=67108864",
    "--ipc=host"
  ],
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
        "RSIP-Vision.nvidia-smi-plus"
      ]
    }
  },
  "mounts": [
    "source=/raid/vllm,target=/app/vllm,type=bind,consistency=cached"
  ],
  "postStartCommand": "vllm serve openai/gpt-oss-120b --gpu-memory-utilization 0.95 --tensor-parallel-size 2 --download-dir /app/vllm --port 8008"
}
```

---

### 2. Dockerfile

Create `.devcontainer/Dockerfile`:

```dockerfile
FROM vllm/vllm-openai:gptoss

ENV USERNAME="$USERNAME"
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ Europe/Berlin
ENV VLLM_ATTENTION_BACKEND=TRITON_ATTN_VLLM_V1

COPY . .

RUN pip3 --no-cache-dir install -r requirements.txt
RUN apt-get update && apt-get install -y curl

EXPOSE 8008
```

---

### 3. Python Dependencies

`requirements.txt`:

```
black
pytest
```

Install dependencies inside the container:

```bash
pip install -r requirements.txt
```

---

### 4. Start the DevContainer

1. Open the project in **VS Code**.
2. Click **Reopen in Container** when prompted.
3. The `postStartCommand` will automatically launch **vLLM server** on port `8008`.

---

### 5. Using the Agent

Inside the container:

```bash
 python3 main.py test_project "add comments to all my python files"
```

The agent will use **vLLM** to plan, refactor, and test your project automatically.

---

## ⚡ Usage

Run the CLI with:

```bash
python main.py <project_path> "<user_request>"
```

Example:

```bash
python main.py ./app "Refactor section1.py to extract helper functions"
```

### Workflow

1. `prepare_context` scans your project files.
2. `PlannerAgent` generates a JSON plan of tool calls.
3. `AgentLoop` executes each tool in sequence.
4. Tests run (if available or auto-generated).
5. Changes are applied safely (backup first).

---

## 🛠️ Tools Available

* **create\_file** → Create new source files.
* **backup\_file** → Backup existing files before modifications.
* **update\_imports** → Fix imports across files.
* **refactor\_code** → Apply structured code transformations.
* **run\_tests** → Execute test suite or generated tests.
* **format\_code** → Run `black` to auto-format.

---

## 👨‍💻 Coding

### Development Setup

Install dependencies:

```bash
pip install -r test_project/requirements.txt
```

Run tests:

```bash
pytest
```

Format code:

```bash
black .
```

### How It Works

The agent follows an **OpenAI-like loop**:

1. **Planner Agent** – Receives user request + context → outputs JSON plan.
2. **Agent Loop** – Executes steps sequentially, ensuring dependencies are respected.
3. **Tools** – Low-level operations (create, backup, refactor, imports, tests).
4. **Re-Planning** (future) – If tests fail, the agent can retry with initial context.

---

## 🌍 Roadmap

*

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
