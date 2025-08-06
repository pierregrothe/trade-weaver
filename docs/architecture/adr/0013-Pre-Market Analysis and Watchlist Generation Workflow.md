# **ADR-001: Pre-Market Analysis and Watchlist Generation Workflow**

* **Status:** Accepted  
* **Date:** 2025-08-06  
* **Deciders:** Pierre Grothé, Tommy (AI Assistant)

## **Context and Problem Statement**

The AI Day Trading Agent requires a systematic, automated, and robust process to run before the market opens. The goal is to filter thousands of stocks across multiple exchanges down to a small, data-rich, and actionable watchlist of high-probability candidates for the day. This process must be efficient, scalable, and adhere to the strict, quantitative principles defined in the project's knowledge base.

## **Decision Outcome**

**Chosen option:** "**Parallelized, Multi-Agent Sequential Pipeline**", because it is the most robust, scalable, and efficient architecture that directly implements the principles of modularity and hierarchical control from the knowledge base \[cite: 01\_system\_architecture\_blueprint.md\]. This design guarantees that the rigorous, multi-stage analysis is performed deterministically for each exchange, while leveraging parallel processing to ensure the final watchlist is ready well before the market opens.

### **Positive Consequences**

* **Efficiency:** Scanning multiple exchanges in parallel drastically reduces the overall time required for pre-market analysis.  
* **Scalability:** Adding a new market to the daily scan is a simple configuration change in Firestore, with no changes required to the agent's code.  
* **Reliability & Testability:** The use of a SequentialAgent for the core pipeline ensures every step is executed in the correct order. Each FunctionTool can be unit-tested in isolation.

### **Negative Consequences**

* **Initial Complexity:** The setup requires defining a hierarchy of agents and multiple, distinct tools.  
* **Dependency Management:** The system is critically dependent on the availability of the EODHD API and the Firestore database during the pre-market window.

### **Appendix A: Detailed Workflow Diagram**

sequenceDiagram  
    participant S as Cloud Scheduler  
    participant E as FastAPI Endpoint  
    participant C as TradingDeskCoordinator  
    participant PSA as PreMarketScannerAgent \<br\> (SequentialAgent)  
    participant FS\_Config as Firestore ('exchanges' collection)  
    participant EODHD as EODHD API  
    participant FS\_Watchlist as Firestore ('watchlist' collection)

    S-\>\>E: 1\. Trigger via HTTP POST with JSON payload  
    E-\>\>C: 2\. Invoke run\_async()  
    C-\>\>PSA: 3\. Delegate to sub-agent (in parallel for each exchange)  
      
    PSA-\>\>FS\_Config: 4\. Read Exchange Config (DB Call)  
    FS\_Config--\>\>PSA: Return config (incl. volatility ticker)

    Note over PSA: Begin Sequential Tool Pipeline...

    PSA-\>\>EODHD: 5\. Tool 1: StaticUniverseFilterTool (API Call)  
    EODHD--\>\>PSA: Return filtered list of stocks  
    Note over PSA: 6\. Initialize 'candidate\_list' in Session State

    PSA-\>\>EODHD: 7\. Tool 2: CatalystScoringTool (API Call)\<br\> \*Processes candidates from state\*  
    EODHD--\>\>PSA: Return news/catalyst data  
    Note over PSA: 8\. Enrich list in Session State

    PSA-\>\>EODHD: 9\. Tool 3: CorporateFilingsCheckTool (API Call)\<br\> \*Processes candidates from state\*  
    EODHD--\>\>PSA: Return filings data  
    Note over PSA: 10\. Enrich list in Session State

    PSA-\>\>PSA: 11\. Tool 4: DiversificationAnalysisTool \<br\> \*Reads list from state, calculates clusters\*  
    Note over PSA: 12\. Enrich list with cluster IDs in Session State  
      
    PSA-\>\>FS\_Watchlist: 13\. Persist Final Enriched List (DB Call)  
    FS\_Watchlist--\>\>PSA: Confirm write

    PSA--\>\>C: 14\. Return final status dict  
    C--\>\>E: 15\. Yield final response event  
    E--\>\>S: Return HTTP 200 OK

### **Appendix B: Agent & Tool Definitions**

#### **TradingDeskCoordinator (Orchestrator)**

* **ADK Class:** ParallelAgent  
* **Input:** JSON payload from Cloud Scheduler (e.g., {"task": "run\_pre\_market\_scan", "exchanges": \["TSX", "NASDAQ"\]}).  
* **Task:** For each exchange in the exchanges array, invoke the PreMarketScannerAgent as a parallel sub-agent.  
* **Output:** An aggregated success/failure message after all parallel scans are complete.

#### **PreMarketScannerAgent (Specialist Sub-Agent)**

* **ADK Class:** SequentialAgent  
* **Input:** An exchange symbol (e.g., "TSX").  
* **Task:** Execute the analysis and enrichment tools in a strict sequence.  
* **Output:** Writes the final enriched watchlist to Firestore; returns a status dict to the Coordinator.

### **Appendix C: Detailed Data Schemas**

#### **Daily Watchlist Document (Firestore)**

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

#### **Stock Candidate Object (in candidate\_list)**

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
