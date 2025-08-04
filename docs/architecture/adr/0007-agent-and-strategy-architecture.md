# ADR-0007: Agent and Strategy Architecture

* **Status:** Accepted
* **Date:** 2025-08-04
* **Deciders:** [Your Name], AI Assistant

## Context and Problem Statement

We need a clear, modular, and scalable way to define our AI agents and the trading strategies they use. The design must allow for easy addition of new strategies, user-level configuration, and adhere to best practices for code organization and maintenance, including the separation of prompts from agent logic.

## Considered Options

* **Option 1: Monolithic Agent:** A single, large agent containing all logic, prompts, and tool definitions. This is difficult to maintain and extend.
* **Option 2: Modular Agent Packages with a Strategy Registry:** Define distinct agents for different roles (`Analyzer`, `Executor`). Each agent is a self-contained Python package. Strategies are independent, pluggable modules. Prompts and tools are organized for clarity and reusability.

## Decision Outcome

**Chosen option:** "Option 2: Modular Agent Packages with a Strategy Registry".

### Positive Consequences

* **Clear Separation of Concerns:** Agents, strategies, shared tools, and core logic are all in distinct directories.
* **ADK Compliance:** Structuring each agent as its own package follows Google ADK's recommended design pattern.
* **Prompt Management:** Decoupling prompts into `prompts.py` files makes them easy to manage, version, and refine without touching the agent's core logic.
* **Code Reusability:** A central `src/tools/` directory allows us to write common tools once and have them be used by multiple agents, adhering to the Don't Repeat Yourself (DRY) principle.
* **Extensibility:** This structure makes adding new agents, strategies, or tools a clean and predictable process.

### Implementation Details

The source code will be organized into four main directories within `src/`:

1. **`src/agents/`**: Contains all ADK Agent definitions. Each agent is its own Python package (a directory with `__init__.py`, `agent.py`, and `prompts.py`).
2. **`src/strategies/`**: Contains the implementation of all trading algorithms as distinct Python modules.
3. **`src/tools/`**: Contains shared, reusable functions (tools) that can be imported and used by any agent in the system.
4. **`src/core/`**: Contains shared business logic and interfaces, like the `BrokerInterface`.
