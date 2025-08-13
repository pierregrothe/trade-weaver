# ADR-0007: Agent and Strategy Architecture

* **Status:** Accepted
* **Date:** 2025-08-04
* **Deciders:** [Your Name], AI Assistant

## Context and Problem Statement

We need a clear, modular, and scalable way to define our AI agents and the trading strategies they use. The design must allow for easy addition of new strategies, user-level configuration, and adhere to best practices for code organization and maintenance, including the separation of prompts from agent logic.

## Considered Options

* **Option 1: Monolithic Agent:** A single, large agent containing all logic, prompts, and tool definitions. This is difficult to maintain and extend.
* **Option 2: Modular Agent Packages with a Strategy Registry:** Define distinct agents for different roles (`PreMarketScannerAgent`, `ExecutorAgent`). Each agent is a self-contained Python package. Strategies are independent, pluggable modules. Prompts and tools are organized for clarity and reusability. Non-agentic entry points are handled separately.

## Decision Outcome

**Chosen option:** "Option 2: Modular Agent Packages with a Strategy Registry", with a revised project structure. Instead of a single `src` directory, each agent will be a self-contained, top-level Python package. This enhances modularity and aligns with a multi-agent, multi-package workspace.

### Positive Consequences

*   **Maximum Modularity:** Each agent is a completely independent unit, simplifying development, testing, and deployment.
*   **Clear Ownership:** The boundaries of each agent's responsibilities are clearly defined by the directory structure.
*   **ADK Compliance:** This structure fully embraces the Google ADK philosophy of building agents as distinct, composable packages.
*   **Scalability:** The project can easily scale by adding new top-level agent folders without modifying a central `src` directory.

### Implementation Details

The project's source code will be organized into top-level directories, one for each agent. The first agent being developed is the `pre_market_analysis_agent`.

1.  **`pre_market_analysis/`**: A self-contained Python package for the agent that scans for pre-market opportunities.
    *   `__init__.py`: Makes the directory a package.
    *   `agent.py`: Contains the primary ADK `Agent` definition (e.g., the `PreMarketAnalysis`).
    *   `tools.py`: Contains the `FunctionTool`s used by this specific agent (e.g., tools for data fetching, filtering, and scoring).
    *   `prompts.py`: (Optional) Contains prompts used by the agent, separating them from the core logic.
    *   `schemas.py`: Contains Pydantic models for data structures used within the agent.

2.  **Future Agents:** Other agents, like an `executor` or `post_market_analyzer`, will be created as separate top-level folders following the same structure.

3.  **Shared Libraries:** Common code, such as the `BrokerInterface` or shared utility functions, will be placed in a dedicated top-level `shared_libs/` directory to be imported by any agent, adhering to the Don't Repeat Yourself (DRY) principle.
