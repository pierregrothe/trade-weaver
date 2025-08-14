# Development Roadmap

This document outlines the agile, phased development plan for the Trade Weaver project. The work is structured into four distinct phases, designed to deliver value incrementally, starting with a foundational data pipeline and culminating in an advanced, self-learning trading system.

---

## Phase 1: Foundational Infrastructure & Data Pipeline

**Goal:** To build the core, non-agentic infrastructure required to support all future development. This phase focuses on data, security, and deployment.

-   **Epics:**
    1.  **CI/CD & Environments:**
        -   Implement the `develop` and `main` branch strategy in GitHub.
        -   Create the `trade-weaver-dev` and `trade-weaver-prod` GCP projects.
        -   Build the GitHub Actions workflows for automated testing and deployment to Cloud Run.
    2.  **Identity & Security:**
        -   Configure Firebase Authentication for user management.
        -   Set up Google Secret Manager for storing all API keys and credentials.
        -   Define IAM roles and permissions for services and users.
    3.  **Data Ingestion & Storage:**
        -   Build the `Data Ingestion Service` (Cloud Run) to connect to the EODHD WebSocket.
        -   Configure the Pub/Sub topic (`raw-market-data`) and the Dead-Letter Queue (DLQ).
        -   Set up the Firestore database with the schemas from the Logical Data Model.
        -   Set up the BigQuery dataset and tables based on the Physical Data Model.

**Exit Criteria:** A developer can deploy a simple "hello world" Cloud Run service via the CI/CD pipeline, and it can successfully read secrets from Secret Manager and connect to the Firestore database.

---

## Phase 2: Market Analyst Agent (MVP)

**Goal:** To develop the first autonomous agent, the `MarketAnalystAgent`, to produce the `MarketAnalysisReport`.

-   **Epics:**
    1.  **Agent Scaffolding:**
        -   Create the `pre_market_analysis` Python package with the standard structure (`agent.py`, `tools.py`, `schemas.py`).
        -   Implement the `CoordinatorAgent` to orchestrate the fan-out/fan-in workflow.
    2.  **Analysis Pipeline Implementation:**
        -   Develop the deterministic `FunctionTool`s for each stage of the analysis (Regime Analysis, Gapper Scanning, Enrichment, Clustering).
    3.  **Output Generation:**
        -   Ensure the agent's final output perfectly matches the canonical `MarketAnalysisReport` JSON schema.

**Exit Criteria:** The agent can be triggered via a Pub/Sub message and successfully produces a valid, well-formed `MarketAnalysisReport` JSON object for a given list of exchanges.

---

## Phase 3: Strategy & Execution Agent (MVP)

**Goal:** To build an agent capable of consuming the analysis report and safely executing trades based on a single, well-defined strategy.

-   **Epics:**
    1.  **Broker Integration:**
        -   Develop the `BrokerInterface` in `shared_libs`.
        -   Implement the IBKR version of the interface, wrapping the `ib_insync` library to handle connections and order placement.
    2.  **Execution Agent FSM:**
        -   Build the `ExecutionAgent` using the defined Finite State Machine (FSM) design.
    3.  **Risk Governor:**
        -   Implement the `RiskGovernor` as a `before_tool_callback` to intercept and validate every trade.
    4.  **Initial Strategy Implementation:**
        -   Implement one complete strategy (e.g., Opening Range Breakout) as a `FunctionTool`.

**Exit Criteria:** The `ExecutionAgent` can consume a `MarketAnalysisReport`, generate a trade signal, have it validated by the Risk Governor, and successfully place a bracket order via the IBKR paper trading API.

---

## Phase 4: Advanced Capabilities & UI

**Goal:** To enhance the system with advanced features, additional strategies, and user-facing controls.

-   **Epics:**
    1.  **Management Cockpit (UI):**
        -   Develop the Firebase Studio UI for monitoring agent status, viewing trade logs, and manually triggering actions.
    2.  **Continuous Learning Loop:**
        -   Implement the post-market `LoopAgent` to analyze performance and provide feedback.
    3.  **Strategy Expansion:**
        -   Implement additional trading strategies (Momentum, Mean Reversion) as new `FunctionTool`s.
    4.  **Advanced Data Integration:**
        -   Integrate specialist Level 2/3 data providers to enhance the `MarketAnalystAgent`.