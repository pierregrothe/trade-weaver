# ADR-0013: Pre-Market Analysis and Watchlist Generation Workflow

* **Status:** Accepted
* **Date:** 2025-08-06
* **Deciders:** Pierre Grothé, Tommy (AI Assistant)

## Context and Problem Statement

The AI Day Trading Agent requires a systematic, automated, and robust process to run before the market opens. The goal is to filter thousands of stocks across multiple exchanges down to a small, data-rich, and actionable watchlist of high-probability candidates for the day. This process must be efficient, scalable, and adhere to the strict, quantitative principles defined in the project's knowledge base.

## Decision Outcome

**Chosen option:** "**Serverless Fan-Out/Fan-In Pipeline via Pub/Sub**", because this architecture provides true, scalable parallelism, which is essential for completing scans of multiple exchanges efficiently before the market opens. It aligns perfectly with our event-driven and serverless principles (ADR-0004, ADR-0012) and directly implements the modularity and hierarchical control from the knowledge base \[cite: 01\_system\_architecture\_blueprint.md\].

### Positive Consequences

* **True Parallelism & Efficiency:** Each exchange is processed by a separate, independent Cloud Run instance, drastically reducing the total time required for pre-market analysis.
* **Scalability:** Adding new markets is a simple configuration change in Firestore. Cloud Run will automatically scale the number of parallel workers to match the workload.
* **Reliability & Resilience:** Using Pub/Sub decouples the components. If a scan for one exchange fails, it can be retried without impacting the others.

### Negative Consequences

* **Increased Observability Complexity:** Debugging requires tracing a request across multiple services (Scheduler -> Pub/Sub -> Cloud Run), making structured logging (ADR-0011) essential.
* **Dependency Management:** The system is critically dependent on the availability of the EODHD API, Pub/Sub, and Firestore during the pre-market window.

### Appendix A: Detailed Workflow Diagram

sequenceDiagram
    participant S as Cloud Scheduler
    participant T1 as Pub/Sub Topic ("start-scan")
    participant C as Cloud Run ("Coordinator")
    participant FS_Config as Firestore ('exchanges' collection)
    participant T2 as Pub/Sub Topic ("scan-jobs")
    participant PSA as Cloud Run ("Scanner Agent")
    participant EODHD as EODHD API
    participant FS_Watchlist as Firestore ('watchlist' collection)

    S->>T1: 1. Publishes cron message
    T1->>C: 2. Triggers Coordinator instance
    C->>FS_Config: 3. Reads list of active exchanges
    FS_Config-->>C: Returns ["NASDAQ", "TSX"]

    loop For each exchange
        C->>T2: 4. Publishes job message (e.g., {"exchange": "NASDAQ"})
    end

    Note over T2, PSA: Fan-Out: Pub/Sub triggers multiple parallel instances of the Scanner Agent
    T2->>PSA: 5. Triggers "NASDAQ" instance
    T2->>PSA: 5. Triggers "TSX" instance

    activate PSA
    Note over PSA: Begin Sequential Tool Pipeline...
    PSA->>EODHD: 6. Tool 1: StaticUniverseFilterTool
    EODHD-->>PSA: Return filtered list
    PSA->>EODHD: 7. Tool 2: CatalystScoringTool
    EODHD-->>PSA: Return enriched list
    PSA->>EODHD: 8. Tool 3: CorporateFilingsCheckTool
    EODHD-->>PSA: Return enriched list
    PSA->>PSA: 9. Tool 4: DiversificationAnalysisTool
    Note over PSA: Fan-In: Each instance writes its results independently
    PSA->>FS_Watchlist: 10. Persist Final Enriched List for its exchange
    FS_Watchlist-->>PSA: Confirm write
    deactivate PSA

### Appendix B: Agent & Service Definitions

#### Coordinator (Cloud Run Entrypoint)

* **Trigger:** Pub/Sub Topic (`start-pre-market-scan`).
* **Task:**
    1. Reads the list of exchanges to be scanned from the Firestore `exchanges` collection.
    2. For each exchange, publishes a message to the `pre-market-scan-jobs` Pub/Sub topic.
* **ADK Implementation:** This is a simple, non-agentic Python function.

#### PreMarketScannerAgent (Specialist Service)

* **Trigger:** Pub/Sub Topic (`pre-market-scan-jobs`).
* **ADK Class:** `SequentialAgent`.
* **Input:** A Pub/Sub message containing the exchange to scan (e.g., `{"exchange": "TSX"}`).
* **Task:** Execute the analysis and enrichment tools in a strict sequence for the given exchange.
* **Output:** Writes the final enriched watchlist to Firestore; terminates its Cloud Run instance.

### Appendix C: Detailed Data Schemas

#### Daily Watchlist Document (Firestore)

*This is the schema for the single document created for each pre-market run. The Document ID could be the date, e.g., 2025-08-06.*

{
  // A non-negotiable, timezone-unaware ISO 8601 timestamp marking when the analysis was completed.
  "analysis\_timestamp\_utc": "2025-08-06T13:30:00Z",

  // An array listing the exchange codes included in this specific analysis run.
  "exchanges\_scanned": \["NASDAQ", "TSX"\],

  // The overall market environment snapshot at the time of analysis.
  "market\_regime": {
    "vix\_value": 18.5,
    "vix\_state": "Low\_Volatility",
    "adx\_value": 29.1,
    "adx\_state": "Trending\_Market",
    "time\_state": "Pre-Market"
  },

  // An array of Stock Candidate Objects, representing the full output of the scanning pipeline.
  "candidate\_list": \[ /\* Array of Stock Candidate Objects, see schema below \*/ \]
}

#### Stock Candidate Object (in candidate\_list)

*This is the detailed schema for each individual stock object that is evolved as it moves through the pipeline.*

{
  // \--- Static data from the initial Screener API call \---
  "code": "NVDA",
  "name": "NVIDIA Corporation",
  "exchange": "NASDAQ",
  "sector": "Technology",
  "industry": "Semiconductors",
  "adjusted\_close": 950.50,
  "market\_capitalization": 2350000000000,

  // \--- Key data points for execution strategies \---
  "pre\_market\_high": 965.20,
  "pre\_market\_low": 958.10,

  // \--- Pipeline Status Tracking \---
  // State machine for the stock: "candidate", "failed\_atr", "failed\_catalyst", "failed\_filings", "ranked"
  "status": "ranked",
  // A human-readable reason if the status is a failure. Blank if successful.
  "status\_reason": "",

  // An ephemeral ID for the correlation cluster this stock belongs to for this specific day.
  "correlation\_cluster\_id": "semiconductors\_cluster\_1",

  // \--- Dynamic Scores from each pipeline stage \---
  "pipeline\_scores": {
    "atr\_value": 45.30,
    "catalyst\_score": 9.8,
    "filings\_score": 5.0,
    "final\_rank\_score": 9.2
  },

  // \--- Catalyst Information \---
  // An array, as a stock can have multiple recent news events.
  "catalyst\_details": \[
    {
      "type": "Earnings Beat",
      "headline": "NVIDIA posts record data center revenue, beats EPS estimates by $0.50.",
      "source": "Benzinga",
      "timestamp": "2025-08-06T12:05:00Z"
    },
    {
      "type": "Analyst Upgrade",
      "headline": "Morgan Stanley raises NVIDIA price target to $1100.",
      "source": "Reuters",
      "timestamp": "2025-08-06T12:45:00Z"
    }
  \]
}
