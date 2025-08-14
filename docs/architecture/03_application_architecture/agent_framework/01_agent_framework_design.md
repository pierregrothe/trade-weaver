# Agent Framework Design

This document outlines the core architectural principles and design patterns for building all AI agents within the Trade Weaver platform. It consolidates the key decisions from ADR-0007, ADR-0017, and ADR-0018.

## 1. Core Principle: Separation of Concerns

The agent framework enforces a strict separation of concerns between objective analysis and subjective decision-making.

- **Market Analyst Agents:** These agents are responsible for objective market analysis ONLY. Their terminal output is a structured, unbiased JSON report containing raw data and metrics (e.g., `MarketAnalysisReport`). They have no knowledge of trading strategies, portfolios, or risk.

- **Strategy & Execution Agents:** These agents consume the reports from analyst agents. They are responsible for applying proprietary logic, user-configured risk parameters, and strategy selection models to make trading decisions.

This separation simplifies the design of both types of agents and allows for greater flexibility and scalability.

## 2. Project Structure: Package-per-Agent

To ensure maximum modularity and clear ownership, the project is organized using a **package-per-agent** structure.

- Each distinct agent (e.g., `pre_market_analysis_agent`, `execution_agent`) is a self-contained, top-level Python package.
- This structure simplifies development, testing, and deployment, and aligns with the Google ADK philosophy of building agents as composable packages.

### Shared Libraries

- Common code, such as the `BrokerInterface` contract, shared data schemas, or utility functions, is placed in a dedicated top-level `shared_libs/` directory. This adheres to the Don't Repeat Yourself (DRY) principle and allows any agent to import shared components.

## 3. Agent Design: Deterministic-First

To enhance performance, reliability, and cost-effectiveness, agents are designed with a **"deterministic-first"** approach.

- **LLM for Synthesis:** `LlmAgent`s are used only for tasks that require complex reasoning, synthesis, or analysis of unstructured data (e.g., interpreting the final results of a complex analysis).
- **Code for Orchestration:** Simple tool-calling, data transformation, and workflow orchestration are implemented in pure Python code within custom `BaseAgent` or `SequentialAgent` classes. This avoids the latency, cost, and non-determinism of using an LLM for simple tasks.

## 4. State Management

To ensure state integrity and proper event tracking within the ADK, tools must be designed as pure functions.

- **Tools Return Data:** Tools **must not** directly modify the session state (e.g., `tool_context.state['key'] = value`).
- **Agent Manages State:** Instead, tools should `return` the data they produce. The parent agent that calls the tool is responsible for taking the returned data and updating the session state. This ensures all state changes are properly tracked in the ADK event lifecycle.

## 5. Security & Hardening: Callbacks as Guardrails

The agent framework uses ADK callbacks as a primary mechanism for security and validation.

- **`before_tool_callback`:** Used to intercept and validate the parameters of any tool call before it is executed. This is the implementation pattern for the **Risk Governor**.
- **`before_agent_callback`:** Used for system-wide, global checks that must run before any agent logic. This is the implementation pattern for the **Volatility Circuit Breaker**.

These callbacks provide essential, non-negotiable guardrails that enforce the system's core safety and compliance rules.
