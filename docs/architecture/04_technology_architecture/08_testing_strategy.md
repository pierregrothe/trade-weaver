# Testing Strategy

This document defines the comprehensive testing strategy for the Trade Weaver project. This strategy is essential for ensuring code quality, preventing regressions, and validating the behavior of individual components.

This strategy complements the **Agent Evaluation Methodology**, which focuses on the agent's decision-making process. This document focuses on the correctness of the underlying code.

## 1. Testing Framework

-   **Framework:** **`pytest`** is the standard testing framework for this project due to its power, flexibility, and rich ecosystem of plugins.
-   **Location:** All tests will reside in the top-level `tests/` directory, which will be structured to mirror the main application's package structure.

## 2. Levels of Testing

A multi-layered testing approach will be used to validate the system at different levels of integration.

### Level 1: Unit Tests

-   **Scope:** Test the smallest possible units of code in isolation (e.g., a single function, a method on a class).
-   **Location:** `tests/unit/`
-   **Requirements:**
    -   Every `FunctionTool` and its underlying business logic MUST have comprehensive unit tests.
    -   Any complex utility function or data transformation MUST be unit tested.
    -   External dependencies (like API calls or database connections) MUST be mocked using libraries like `pytest-mock` to ensure the test is isolated.

### Level 2: Integration Tests

-   **Scope:** Test the interaction between multiple components, such as the integration between an agent and its tools, or between a service and a real database.
-   **Location:** `tests/integration/`
-   **Requirements:**
    -   Test agent pipelines (e.g., the `MarketAnalystPipeline`) to ensure the `ToolContext` and state are passed correctly between steps.
    -   Test the `BrokerInterface` against the live paper trading APIs (IBKR and others) to validate the contract.
    -   These tests will run against the `development` GCP project resources (e.g., a test Firestore instance).

### Level 3: End-to-End (E2E) Tests

-   **Scope:** Test the entire workflow of a use case from start to finish.
-   **Location:** `tests/e2e/`
-   **Example Use Case:**
    1.  Programmatically publish a `COMMAND_RUN_ANALYSIS` message to the development Pub/Sub topic.
    2.  Poll a results location (e.g., a specific Firestore document) until the `MarketAnalystAgent` has completed its run.
    3.  Validate that the final `MarketAnalysisReport` is correctly structured and contains the expected data.

## 3. CI/CD Integration

-   **Execution:** The full suite of unit and integration tests will be executed automatically by **GitHub Actions** on every pull request against the `develop` and `main` branches.
-   **Gating:** A pull request **cannot be merged** if any test fails. This provides a critical quality gate and prevents regressions from being introduced into the main codebase.
