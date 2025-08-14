# ADR-0018: Refined Market Analyst Agent Architecture

* **Status:** Accepted
* **Date:** 2025-08-14
* **Deciders:** Pierre Grothé, AI Assistant
* **Supersedes:** ADR-0013

## 1. Context and Problem Statement

The initial design for the pre-market analysis (ADR-0013) defined a single-stage parallel workflow per exchange that produced a "watchlist" written to Firestore. Subsequent design refinements revealed several areas for improvement:

1. **Separation of Concerns:** The agent's role was conflated with making trading recommendations. Its role must be strictly limited to objective market analysis.
2. **Performance Bottleneck:** A monolithic analysis pipeline per exchange does not maximize parallelism. The discovery of candidates can be done much faster than the deep enrichment of each one.
3. **Output Rigidity:** Writing directly to Firestore and pre-calculating stateful scores (e.g., `vix_state`) created a rigid output. The system requires a flexible, universal output format (JSON) and should provide raw data, not interpretations, to empower the downstream consumer.
4. **Risk Management Blindspot:** The initial design did not account for identifying correlated risk among potential candidates.

## 2. Decision Outcome

**Chosen option:** We will adopt a **three-stage, multi-fan-out agent architecture** that clearly separates the responsibilities of discovery, enrichment, and correlation analysis. The agent's sole output will be a **structured JSON `MarketAnalysisReport`** containing objective raw data.

### Key Architectural Changes

1. **Strict Role Definition:** The Market Analyst Agent's responsibility ends with the production of the JSON report. It has no knowledge of trading strategies or user preferences.
2. **Multi-Stage Fan-Out Workflow:**
    * **Stage 1 (Discovery):** A fast, parallel scan of each exchange to identify all potential "gapping" instruments.
    * **Stage 2 (Enrichment):** A second, massively parallel fan-out to enrich *each discovered ticker* with fundamental data, news, and raw technical indicator values.
    * **Stage 3 (Clustering):** A final step to calculate a correlation matrix and assign a `correlation_cluster_id` to each instrument.
3. **JSON Output:** The agent's terminal output is a single JSON document. The schema for this document is the new API contract for any downstream consumer. Firestore is now only used for reading agent configurations.
4. **Raw Data, Not Scores:** The JSON output provides raw metric values (e.g., `vix_value`, `rsi_14d`), not pre-calculated state interpretations. This gives the consuming agent maximum flexibility.

### Positive Consequences

* **Maximum Parallelism & Speed:** The new architecture is significantly faster and more efficient.
* **Clear Separation of Concerns:** Simplifies the design of both the Analyst Agent and the downstream Strategy Agent.
* **Flexibility & Scalability:** The JSON output is a universal, flexible contract. The consuming agent can apply any logic it needs to the raw data without requiring changes to the analyst agent.
* **Enhanced Risk Awareness:** The inclusion of correlation clustering provides a critical data point for the downstream agent's risk management module.

### Negative Consequences

* The workflow orchestration in the `CoordinatorAgent` is slightly more complex, managing two stages of fan-out/fan-in. This is a justifiable trade-off for the performance gains.
