# ADR-0017: Agent Refactoring and Hardening

* **Status:** Accepted
* **Date:** 2025-08-12
* **Deciders:** Jules 2.0, Project Lead

## Context and Problem Statement

A thorough review of the `trade_weaver` and `market_analyst` agents revealed several areas where the implementation deviates from the best practices of the Google ADK v1.10.0+ framework and the project's own mandate. These deviations introduce potential brittleness, reduce maintainability, and pose security risks. The primary issues identified are:

1.  **Inconsistent Agent Logic:** The `CoordinatorAgent`'s implementation in `agent.py` is a dynamic orchestrator, but its corresponding `prompt.py` file contains an outdated prompt for a simple delegator, causing confusion.
2.  **Improper State Management:** Tools in `market_analyst/tools.py` directly modify the session state (`tool_context.state['key'] = value`), which is an anti-pattern that bypasses the ADK's tracked event lifecycle.
3.  **Lack of Security and Validation Guardrails:** The agents lack callbacks (`before_tool_callback`, `before_model_callback`) to validate inputs and prevent potential prompt injection attacks.

This ADR outlines the decisions to refactor the existing implementation to align with ADK best practices, improve robustness, and enhance security.

## Decision Outcome

**Chosen option:** "Comprehensive Refactoring to ADK Best Practices", because this approach directly addresses all identified issues and aligns the codebase with the project's core principles of building a robust, reliable, and testable system.

### Positive Consequences

* **Improved Clarity and Maintainability:** Consolidating prompts into agent definitions makes the agent's purpose clear and self-contained.
* **Enhanced State Integrity:** Refactoring tools to return data ensures all state changes are tracked through the ADK event lifecycle, preventing race conditions and making debugging easier.
* **Increased Security and Robustness:** Implementing callbacks provides essential guardrails for validating inputs and preventing common vulnerabilities.
* **Full Compliance with Project Mandate:** This refactoring brings the codebase into full compliance with the explicit requirements of the project.

### Negative Consequences

* **Requires careful refactoring:** The changes to tool signatures and state access will require careful updates to the agents that use them.

## Implementation Details

The refactoring will be implemented across three key areas:

1.  **Prompt Consolidation for `CoordinatorAgent`:**
    *   The file `trade_weaver/prompt.py` will be deleted.
    *   A concise, accurate instruction will be added to the `instruction` parameter of the `CoordinatorAgent` in `trade_weaver/agent.py`.

2.  **State Management Refactoring in `market_analyst` Tools:**
    *   All tools in `trade_weaver/sub_agents/market_analyst/tools.py` will be modified.
    *   Instead of `tool_context.state['key'] = value`, each tool will `return` a dictionary containing the data it produces.
    *   The `CustomToolCallingAgent` and other agents in `market_analyst/agent.py` will be updated to handle the returned data and place it into the state using the appropriate `output_key`.

3.  **Implementation of Callbacks for Guardrails:**
    *   A `before_tool_callback` will be added to the `MarketAnalystPipeline`. This callback will inspect the `FunctionCall` event and validate the `exchange` parameter for the `get_exchange_details_tool`, ensuring it's a valid, non-malicious string.
    *   A `before_model_callback` will be added to the `CoordinatorAgent` to serve as an input guardrail, checking the user-provided JSON for any signs of prompt injection before it is processed.
