# ADR-0013: Deterministic-First Market Analyst Pipeline

**Date**: 2025-08-08

**Status**: Implemented

## Context

The `MarketAnalystPipeline` was initially designed with `LlmAgent`s for most of its sequential tasks. This architecture, while functional, led to several issues:

- **High Latency**: Each step involving an `LlmAgent` incurred a network roundtrip to the Gemini API.
- **Rate Limiting**: The high frequency of API calls increased the risk of hitting rate limits.
- **Cost**: Every LLM call has an associated financial cost.
- **Non-Determinism**: Simple tasks like tool calling were subject to the LLM's interpretation, leading to potential brittleness.

The goal was to refactor the pipeline to be hyper-efficient, reliable, and cost-effective by using LLMs only for tasks that require complex reasoning and synthesis.

## Decision

We have decided to refactor the `MarketAnalystPipeline` to adopt a "deterministic-first" approach. This involves replacing all `LlmAgent`s responsible for simple tool-calling with custom `BaseAgent`s that execute this logic in pure Python code.

The new architecture is composed of the following key components:

1. **`CustomToolCallingAgent`**: A reusable, deterministic agent that takes a specific tool in its constructor and calls it directly. This agent is used for simple, single-tool-calling steps.

2. **`StockDataEnrichmentAgent`**: A custom, deterministic agent that orchestrates a multi-step tool-calling process in code: it first finds pre-market movers and then iterates through the results to fetch detailed data for each stock.

3. **Refactored Sub-Pipelines**:
    - `MarketRegimeSubPipeline`: Now uses `CustomToolCallingAgent` instances for parallel data gathering (`VIX`, `ADX`, `Time`). The `regime_synthesizer` remains an `LlmAgent`, as it performs a complex synthesis task.
    - `StockScannerSubPipeline`: Now consists of only two steps: the deterministic `StockDataEnrichmentAgent` followed by the `synthesis_scanner` `LlmAgent`, which analyzes the fully enriched data.

## Envisioned Workflow

```mermaid
sequenceDiagram
    participant CoordinatorAgent
    participant Session State
    box rgba(230, 240, 255, 0.8) Dynamically Created ParallelAgent
        participant MarketAnalystPipeline (for NASDAQ)
        participant MarketAnalystPipeline (for TSX)
    end
    participant Final Report

    CoordinatorAgent->>CoordinatorAgent: 1. Receives payload `exchanges: ["NASDAQ", "TSX"]`

    CoordinatorAgent->>+ParallelAgent: 2. **(Fan-Out)** Dynamically builds a ParallelAgent with two complete, self-contained pipeline instances.

    Note right of ParallelAgent: Both pipelines run their FULL internal sequence concurrently in the SAME session.

    ParallelAgent->>+MarketAnalystPipeline: 3a. **NASDAQ Pipeline Executes:**<br/>1. Fetches its details.<br/>2. Calculates its market regime.<br/>3. Scans for its stocks.<br/>4. Assembles its complete `ExchangeAnalysisResult`.
    MarketAnalystPipeline-->>Session State: Writes the single, complete result to **`result_NASDAQ`**.

    ParallelAgent->>+MarketAnalystPipeline: 3b. **TSX Pipeline Executes (in parallel)...**<br/>...and writes its complete result to **`result_TSX`**.

    ParallelAgent-->>-CoordinatorAgent: 4. Parallel execution completes.

    CoordinatorAgent->>Session State: 5. **(Fan-In)** Reads the complete `ExchangeAnalysisResult` objects from `result_NASDAQ` and `result_TSX`.

    CoordinatorAgent->>Final Report: 6. Assembles the final `DailyWatchlistDocument`.

    CoordinatorAgent-->>External System: 7. Returns final, aggregated JSON report.
```

## Consequences

- **Positive**:
  - **Reduced LLM Calls**: The number of LLM calls per pipeline run is reduced to the absolute minimum (two).
  - **Increased Speed**: The pipeline is significantly faster due to the elimination of network latency for most steps.
  - **Improved Reliability**: The pipeline is more deterministic and less prone to errors from LLM misinterpretations.
  - **Lower Cost**: Fewer LLM calls result in lower operational costs.

- **Negative**:
  - The `CoordinatorAgent` must be robust enough to handle cases where all parallel pipelines fail. The fan-in logic needs to explicitly check for an empty result set and return a final "error" status if no pipelines succeeded.

## Data Schemas

*The canonical, implementation-ready Pydantic models and Firestore schemas are defined in the **[Firestore Database Schema](../02-firestore-database-schema.md)** document. The schemas below are for illustrative purposes within this ADR.*

### MarketRegimeState

```python
class MarketRegimeState(BaseModel):
    """A structured representation of the market's current regime."""
    exchange: str
    vix_value: float
    vix_state: str
    adx_value: float
    adx_state: str
    time_of_day_state: str
    regime_code: str
    timestamp: str
```

### StockCandidateObject

```python
class StockCandidateObject(BaseModel):
    """
    Detailed schema for each individual stock candidate that is evolved as it
    moves through thepipeline.
    """
    code: str
    name: str
    exchange: str
    sector: str
    industry: str
    adjusted_close: float
    market_capitalization: int
    pre_market_high: float
    pre_market_low: float
    status: str
    status_reason: str
    correlation_cluster_id: str
    pipeline_scores: List[PipelineScore]
    catalyst_details: List[CatalystDetail]
```

### StockCandidateList

```python
class StockCandidateList(BaseModel):
    """A wrapper for a list of stock candidates, used for LLM output."""
    candidates: List[StockCandidateObject]
```

### ExchangeAnalysisResult

```python
class ExchangeAnalysisResult(BaseModel):
    """The complete analysis result for a single exchange worker pipeline."""
    market_regime: MarketRegimeState
    candidate_list: List[StockCandidateObject]
```

### DailyWatchlistDocument

```python
class DailyWatchlistDocument(BaseModel):
    """
    The final, aggregated watchlist document for a given day, containing
    the analysis results for each scanned exchange.
    """
    analysis_timestamp_utc: str
    exchanges_scanned: List[str]
    analysis_results: List[ExchangeAnalysisResult]
```
