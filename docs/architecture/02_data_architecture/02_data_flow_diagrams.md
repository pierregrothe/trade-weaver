# Data Flow Diagrams

This document visualizes the flow of data through the Trade Weaver system, from external sources to internal processing and storage. These diagrams help to clarify how components interact with data and where data transformations occur.

## 1. High-Level Data Flow (End-to-End)

This diagram shows the overall flow of data from external providers, through the ingestion and analysis pipelines, to the point of consumption by the trading agents.

```mermaid
graph TD
    subgraph "External Data Providers"
        EODHD_API[EODHD API]
        IBKR_API[IBKR API]
        Specialist_API[Specialist L3 Data API]
    end

    subgraph "GCP Ingestion Layer"
        IngestionService[Data Ingestion Service (Cloud Run)]
        RawDataTopic[Pub/Sub: Raw Market Data]
    end

    subgraph "GCP Processing & Storage Layer"
        MarketAnalystAgent[Market Analyst Agent (Cloud Run)]
        ExecutionAgent[Strategy & Execution Agent (Cloud Run)]
        FirestoreDB[Firestore Database]
        TradeLogs[Trades Collection]
        ConfigStore[Configuration Collections]
    end

    %% Data Flows
    EODHD_API -- EOD, Fundamentals, News --> IngestionService
    IBKR_API -- Real-Time L1/L2 --> IngestionService
    Specialist_API -- Real-Time L3 --> IngestionService
    
    IngestionService -- Publishes Raw Data --> RawDataTopic
    
    RawDataTopic -- Subscribes to --> MarketAnalystAgent
    MarketAnalystAgent -- Reads Config --> ConfigStore
    MarketAnalystAgent -- Produces --> MarketAnalysisReport[JSON: MarketAnalysisReport]
    
    MarketAnalysisReport -- Consumed by --> ExecutionAgent
    ExecutionAgent -- Reads Config --> ConfigStore
    ExecutionAgent -- Writes to --> TradeLogs
    
    FirestoreDB -- Contains --> TradeLogs
    FirestoreDB -- Contains --> ConfigStore
```

### Description of Flow

1.  **Ingestion:** A dedicated `Data Ingestion Service` connects to all external APIs (EODHD, IBKR, etc.) to source historical, fundamental, and real-time market data.
2.  **Decoupling:** The ingestion service publishes all raw data into a central `Pub/Sub` topic. This decouples the data sources from the data consumers, adding resilience and scalability.
3.  **Analysis:** The `Market Analyst Agent` subscribes to the raw data topic. It reads its configuration from Firestore, processes the data through its multi-stage pipeline, and produces a single, objective `MarketAnalysisReport` as a JSON object.
4.  **Execution:** The `Strategy & Execution Agent` consumes this JSON report, applies its own strategic logic and risk management rules (also read from Firestore), and executes trades.
5.  **Logging:** All executed trades are recorded as immutable logs in the `Trades` collection within Firestore.
