# ADR-0017: Agent Refactoring and Hardening

* **Status:** Accepted
* **Date:** 2025-08-12
* **Deciders:** Jules 2.0, Project Lead

## Context and Problem Statement

As part of the architectural shift to a package-per-agent structure (ADR-0007), a review of the initial agent design is required to ensure it aligns with Google ADK v1.10.0+ best practices from the start. The design for the new `PreMarketAnalysisAgent` must avoid potential brittleness, be maintainable, and include security guardrails. The primary issues to address proactively are:

1.  **Inconsistent Agent Logic:** The agent's implementation in `agent.py` must be the single source of truth for its orchestration logic, and any associated prompts must be consistent and clear.
2.  **Improper State Management:** Tools must not directly modify the session state (`tool_context.state['key'] = value`). This is an anti-pattern that bypasses the ADK's tracked event lifecycle.
3.  **Lack of Security and Validation Guardrails:** The agent must have callbacks (`before_tool_callback`, `before_model_callback`) to validate inputs and prevent potential prompt injection attacks.

This ADR outlines the decisions to build the new `PreMarketAnalysisAgent` in alignment with ADK best practices, improving robustness, and enhancing security from day one.

## Decision Outcome

**Chosen option:** "Build with ADK Best Practices", because this approach directly addresses all identified issues and aligns the codebase with the project's core principles of building a robust, reliable, and testable system.

### Positive Consequences

*   **Improved Clarity and Maintainability:** Defining a clear purpose for the agent in its instruction makes it self-contained and understandable.
*   **Enhanced State Integrity:** Designing tools to return data ensures all state changes are tracked through the ADK event lifecycle, preventing race conditions and making debugging easier.
*   **Increased Security and Robustness:** Implementing callbacks provides essential guardrails for validating inputs and preventing common vulnerabilities.
*   **Full Compliance with Project Mandate:** This approach ensures the codebase is in full compliance with the explicit requirements of the project from the outset.

### Negative Consequences

*   This requires slightly more boilerplate for tool and agent definitions but pays dividends in long-term maintainability.

## Implementation Details

The best practices will be implemented in the new `pre_market_analysis_agent` package:

1.  **Clear Agent Instruction:**
    *   The file `pre_market_analysis_agent/prompts.py` will be avoided initially.
    *   A concise, accurate instruction will be added to the `instruction` parameter of the `PreMarketAnalysisAgent` in `pre_market_analysis_agent/agent.py`.

2.  **State Management Best Practices:**
    *   All tools in `pre_market_analysis_agent/tools.py` will be designed to be functional.
    *   Instead of modifying state, each tool will `return` a dictionary or Pydantic model containing the data it produces.
    *   The agent orchestrating the tools (e.g., a `SequentialAgent` or custom `BaseAgent`) will be responsible for taking the returned data and placing it into the state using the appropriate `output_key` or manual state update.

3.  **Implementation of Callbacks for Guardrails:**
    *   A `before_tool_callback` will be added to the `PreMarketAnalysisAgent`. This callback will inspect the `FunctionCall` event and validate parameters for any tool call (e.g., ensuring an `exchange` string is valid and not malicious).
    *   A `before_model_callback` will be added to the `PreMarketAnalysis` to serve as an input guardrail, checking any user-provided JSON for signs of prompt injection before it is processed.
