# Application Component Model and Diagrams

This document provides a holistic view of the Trade Weaver ecosystem, illustrating the key software components and their interactions.

## 1. Master System Architecture

This diagram provides a high-level view of the entire ecosystem, illustrating the relationships between Google Cloud services, external data providers, and the core trading agent.

```mermaid
graph TD
    subgraph "Google Cloud Platform"
        subgraph "Trading Agent Service (Cloud Run)"
            A[CoordinatorAgent]
            B[MarketAnalystPipeline]
            C[ExecutionAgent FSM]
            D[RiskGovernor]
        end

        subgraph "Data Services"
            E[Data Ingestion Service (Cloud Run)]
            F[Firestore Database]
            G[Pub/Sub Topics]
        end

        H[Cloud Scheduler]
        I[Google Secret Manager]
    end

    subgraph "External Services"
        J[User Interface]
        K[EODHD API]
        L[IBKR API]
        M[Databento/dxFeed API]
    end

    %% Flows
    H -- Triggers Daily Run --> A
    J -- Sends Manual Commands --> G
    A -- Reads Config From --> F
    A -- Spawns --> B
    B -- Generates --> F(DailyWatchlists)
    C -- Reads --> F(DailyWatchlists)
    C -- Executes Trades Via --> L
    D -- Intercepts & Validates Trades For --> C
    
    K -- Foundational Data --> E
    L -- Real-Time L1/L2 Data --> E
    M -- Real-Time L3 Data --> E
    E -- Publishes Raw Data --> G
    B -- Subscribes to Data --> G
    C -- Subscribes to Data --> G

    A -- Reads Secrets From --> I
    E -- Reads Secrets From --> I

```

### Component Descriptions

*   **Cloud Scheduler:** Triggers the `CoordinatorAgent` to start the pre-market analysis at a scheduled time.
*   **Trading Agent Service (Cloud Run):** The core containerized application running the ADK agents.
    *   `CoordinatorAgent`: The master agent that orchestrates the entire workflow.
    *   `MarketAnalystPipeline`: The worker agent that performs analysis on a specific exchange.
    *   `ExecutionAgent FSM`: The state machine that manages intraday trading logic.
    *   `RiskGovernor`: The callback that enforces all risk management protocols.
*   **Data Services (GCP):**
    *   `Data Ingestion Service`: A separate service responsible for connecting to all external data provider APIs and streaming the raw data into the system via Pub/Sub.
    *   `Firestore Database`: The system's central database for all configuration, operational data, and trade logs.
    *   `Pub/Sub Topics`: The messaging backbone that decouples data ingestion from the trading agent.
*   **External Services:**
    *   `User Interface`: The web-based UI for monitoring and manual control.
    *   `EODHD/IBKR/Specialists`: The various external data providers.

---

## 2. Premarket Analysis Workflow Diagrams

These diagrams illustrate the two distinct, market-specific pipelines executed by the `ExchangeAnalysisPipeline` component.

### 2.1 Introspective Pipeline (e.g., NASDAQ, NYSE)

This model is used for markets with active pre-market trading. It analyzes the stock's *own* price and volume data to *confirm* the quality of an observed move.

```mermaid
flowchart TD
    A[Start: Stock Ticker] --> B{Initial Filter Check};
    B -- Pass --> C[Ingest Real-Time L1 Data from IBKR];
    C --> D[Ingest News from EODHD];
    D --> E[Calculate Catalyst Score];
    C --> F[Calculate Price/Volume Metrics];
    F --> G["`Chart_Clarity_Score` (5/7 Metrics)"];
    G --> H{L2 Data Available?};
    H -- No (IBKR L2) --> I[Approximate Order Flow];
    H -- Yes (Specialist L3) --> J[Calculate Full Order Flow Metrics];
    I --> K[Combine All Scores];
    J --> K;
    E --> K;
    K --> L[Final Ranking];
    L --> M[Output: Ranked Watchlist];
```

### 2.2 Extrospective Pipeline (e.g., TSX, LSE, Deutsche Börse)

This model is used for markets with an opening auction. It uses external, correlated instruments to *predict* the outcome of the opening auction.

```mermaid
flowchart TD
    A[Start: Stock Ticker] --> B{Find Proxy Instrument(s)};
    B -- Found --> C[Ingest Real-Time L1 Data for US-listed ETF Proxy];
    C --> D[Calculate Macro Catalyst Score];
    C --> E[Calculate US Sector Sentiment Score];
    D --> F[Combine Scores];
    E --> F;
    F --> G{Order Imbalance Data Available?};
    G -- No --> H[Final Ranking];
    G -- Yes (Specialist L2/L3) --> I[Calculate Order Imbalance Score];
    I --> J[Re-weight and Combine All Scores];
    J --> H;
    H --> K[Output: Predicted Gapper List];
```
