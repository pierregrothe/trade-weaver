# Code and Project Structure

This document defines the standard file and folder structure, naming conventions, and coding style for all Python code in the Trade Weaver project.

## 1. Top-Level Project Structure

The project uses a modular, package-per-agent structure at the top level.

```
trade-weaver/
├── .github/              # CI/CD workflows
├── .venv/                # Python virtual environment
├── docs/
│   ├── architecture/     # The structured architecture documents
│   └── ...
├── pre_market_analysis/  # Example of an Agent Package
│   ├── __init__.py
│   ├── agent.py
│   ├── tools.py
│   └── schemas.py
├── execution_agent/      # Example of another Agent Package
│   └── ...
├── shared_libs/          # Shared code accessible by all agents
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── broker_interface.py
│   └── utils/
│       └── ...
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml        # Project dependencies and metadata
└── ...
```

## 2. Naming Conventions

Consistency in naming is critical for readability. The following conventions MUST be followed:

| Element | Case Style | Example |
| :--- | :--- | :--- |
| Packages / Modules | `snake_case` | `pre_market_analysis`, `broker_interface.py` |
| Classes | `PascalCase` | `MarketAnalystAgent`, `MarketAnalysisReport` |
| Functions / Methods | `snake_case` | `run_analysis`, `get_vix_value` |
| Variables / Arguments | `snake_case` | `vix_value`, `correlation_matrix` |
| Constants | `UPPER_SNAKE_CASE` | `VIX_THRESHOLD = 35` |

## 3. Agent Package Structure (`<agent_name>/`)

Each agent package should follow this internal structure:

-   **`agent.py`**: Contains the primary ADK `Agent` definitions (e.g., `SequentialAgent`, `LlmAgent`, custom `BaseAgent`). This is the orchestrator.
-   **`tools.py`**: Contains the `FunctionTool`s used by the agent. For complex agents, this can be broken into multiple tool files (e.g., `data_tools.py`, `analysis_tools.py`).
-   **`schemas.py`**: Contains all Pydantic models used for data validation and as schemas for `FunctionTool` inputs and outputs.

## 4. Coding Style and Type Hinting

-   **Style Guide:** All Python code should adhere to **PEP 8**.
-   **Linter / Formatter:** **Ruff** will be used for both linting and automatic formatting to ensure consistency.
-   **Type Hinting:** Type hints are **mandatory** for all function signatures and variable declarations. This improves code clarity, allows for static analysis, and is essential for the ADK framework.
