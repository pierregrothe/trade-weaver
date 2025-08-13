# [CONCEPT: System_Architecture] AI Agent System Architecture Blueprint

This document outlines a robust, scalable, and decoupled architecture for the AI day trading agent, built on a tech stack of Python, Google Cloud Platform (GCP), and Firebase.

### [PRINCIPLE: Architectural_Design] Core Architectural Principles

- **[DESIGN: Modular] Modular & Decoupled:** The system must be architected using a modular, microservices-based approach. Core functions (Data Ingestion, Strategy Execution, Risk Management, Order Management) must be discrete, independently deployable services to enhance fault isolation and scalability.
- **[DESIGN: Hierarchical_Control] Hierarchical Control:** The architecture is explicitly hierarchical. The **[MODULE: Risk_Governor]** must reside at the apex. Strategy modules generate "trade proposals," which are validated and sized by the Governor before being passed to the Order Execution Service.
- **[DESIGN: Event_Driven] Event-Driven & Serverless:** The architecture is event-driven, leveraging serverless components like GCP Cloud Run to be cost-efficient, scalable, and resilient.

### [CONCEPT: Implementation_Blueprint] Implementation Blueprint (GCP & Firebase)

- **[MODULE: Real_Time_Ingestion] Real-Time Ingestion (WebSockets):**
    1. A dedicated **GCP Cloud Run** service runs an async Python client (`eodhdc`).
    2. It establishes a persistent WebSocket connection to the data provider.
    3. Received real-time messages are immediately published to a **GCP Pub/Sub** topic (e.g., `real-time-market-data`).
    4. The AI Agent application, as a separate Cloud Run service, subscribes to this Pub/Sub topic. This decouples data ingestion from trading logic.

- **[MODULE: Batch_Ingestion] Batch & Historical Ingestion:**
    1. A **GCP Cloud Scheduler** job triggers a separate Cloud Run service nightly/weekly.
    2. This service calls bulk API endpoints to fetch EOD prices, fundamentals, etc.
    3. Data is written to a primary analytical data store like **BigQuery** for model training.

- **[MODULE: Data_Validation] Data Validation & State Management:**
    1. A dedicated data validation service subscribes to both real-time and batch data streams before they are committed to the primary database. It checks for schema correctness, identifies statistical outliers (e.g., price spikes > 10 * ATR), and flags data gaps.
    2. **Firebase Firestore** is used as the state and configuration store, holding trading parameters (risk limits, asset whitelist) and trade logs.

### [CONCEPT: ADK_Implementation] ADK Implementation Strategy

The core AI Agent application itself should be built using the Google ADK framework, mapping architectural concepts to specific ADK classes.

- **[ADK: Root_Agent] Root Agent:** The main application will be a root `LlmAgent` or a `SequentialAgent` that orchestrates the overall daily cadence (pre-market, open, close).
- **[ADK: Risk_Governor] Risk Governor Implementation:** The hierarchical risk control is implemented using ADK **Callbacks**. A `before_tool_callback` is attached to the root agent. This callback intercepts all trade execution `FunctionTool` calls. Inside the callback, the logic of the Risk Governor (1% rule, portfolio heat check, etc.) is executed to validate and size the trade before allowing the tool to run.
- **[ADK: Strategy_Portfolio] Strategy Portfolio:** The agent will contain multiple strategy modules. This can be implemented as a set of specialized `FunctionTool`s (e.g., `execute_momentum_strategy`, `execute_mean_reversion_strategy`). The root `LlmAgent` is instructed to call the appropriate tool based on the market state (time of day, VIX level), which is stored in `tool_context.state`.

[SOURCE_ID: EODHD for AI Trading Platform, Section 1.3 & 5.3]
[SOURCE_ID: ADK Trading Modules Implementation, Introduction]
