# Development Plan

This document outlines the agile, phased development plan for the Trade Weaver project. The work is structured into three main Epics, each representing a major stage of the project's lifecycle, from a Minimum Viable Product to a feature-rich, institution-grade system.

This plan adopts a declarative, workflow-centric approach, utilizing **Google Jules** as the primary framework for defining, evaluating, and deploying agents and their components. The architecture of each component will be heavily inspired by the best practices and patterns found in the official Google ADK Samples.

---

### Guiding Principles for Agent Design

This development plan adheres to the following core principles to ensure the created agents are efficient, reliable, and cost-effective:

1. **Deterministic by Default:** Agents and tools will be implemented with deterministic, coded logic wherever possible. `LlmAgent`s and calls to large language models will be reserved exclusively for tasks that require complex reasoning, synthesis, or natural language understanding. Tasks like data retrieval, calculation, and structured transformations will be handled by deterministic `FunctionTool`s within `SequentialAgent` or custom `BaseAgent` workflows.
2. **Read-Only Agents:** As established, agents read data from data sources like Firestore but do not write back to them. The responsibility for persisting an agent's output lies with the client application that invokes the agent.

---

## Phase 1: The Pre-Market Analysis (MVP)

* **Epic:** Develop the first autonomous agent, the `PreMarketAnalysis`, to establish the core project structure and deliver the foundational analysis pipeline.

  * **Agent Definition: `PreMarketAnalysis`**
    * **Intent:** To serve as the master orchestrator for the pre-market scanning process. It receives a request to scan a set of markets and is responsible for coordinating the parallel execution of analysis pipelines and aggregating the final results into a definitive daily watchlist.
    * **ADK Class:** `google.adk.agents.BaseAgent` (A custom agent with deterministic orchestration logic).
    * **ADK Sample Inspiration:** The orchestration logic will be similar to the **`camel`** sample, where a master agent coordinates tasks among multiple specialist agents. The overall structure of the agent package will follow the pattern of the **`data-science`** and **`financial-advisor`** samples.
    * **Input:** A JSON object from the user or a triggering system containing `{"exchanges": ["NASDAQ", "TSX"]}`.
    * **Output:** A final `Content` event containing the `DailyWatchlistDocument`. It is the responsibility of the client application to persist this output.
      * **Schema Reference:** `docs/architecture/02-firestore-database-schema.md`
    * **Callbacks:**
      * `InputGuardrailCallback` (`before_agent_callback`): Checks the incoming JSON for schema validity and potential injection attacks. Inspired by the **`llm-auditor`** sample.

  * **Component Definition: `ExchangeAnalysisPipeline` (Internal Workflow)**
    * **Intent:** To perform the complete, multi-stage analysis for a single stock exchange.
    * **ADK Class:** `google.adk.agents.SequentialAgent`. This deterministic pipeline is composed of `FunctionTool`s.
    * **ADK Sample Inspiration:** This sequential, multi-tool pipeline mirrors the approach of the **`academic-research`** agent.

    * **Workflow Step 1: Market Regime Analysis**
      * **Tool:** `GetMarketRegime`
      * **Intent:** To establish the broad market context using deterministic rules.
      * **Knowledge Base Reference:** `01_foundations/05_market_regime_analysis_module.md`
      * **Pseudocode (Tool Implementation):**

                ```
                FUNCTION GetMarketRegime(exchange):
                  vix = FETCH_VIX_VALUE_FROM_API()
                  adx = FETCH_ADX_VALUE_FROM_API(proxy_for_exchange)
                  time_state = GET_CURRENT_TIME_OF_DAY_STATE()

                  // Deterministic rule-based classification
                  vix_state = CLASSIFY_VIX_STATE(vix) // e.g., IF vix > 30 -> "High_Volatility"
                  adx_state = CLASSIFY_ADX_STATE(adx) // e.g., IF adx > 25 -> "Trending_Market"

                  regime_code = f"{time_state}_{adx_state}_{vix_state}"

                  RETURN MarketRegimeState(
                    vix_value=vix,
                    vix_state=vix_state,
                    adx_value=adx,
                    adx_state=adx_state,
                    time_of_day_state=time_state,
                    regime_code=regime_code
                  )
                ```

    * **Workflow Step 2: Stock Universe Filtering & Enrichment**
      * **Tool:** `EnrichStockUniverse`
      * **Intent:** To filter the exchange, find gappers, and enrich them with catalyst and quality scores.
      * **Knowledge Base Reference:** `02_operational_playbook/02a_pre_market_analysis_framework_deep_dive.md`
      * **ADK Sample Inspiration:** The tool's internal NLP logic for catalyst scoring will be based on the principles of the **`RAG`** sample, retrieving relevant news and synthesizing a score. This is a valid use of a specialized model (e.g., FinBERT), not a general-purpose LLM.

    * **Workflow Step 3: Assemble Final Result**
      * **Tool:** `AssembleExchangeResult`
      * **Intent:** To combine the outputs of the previous steps into a single, structured result object for this exchange.

---

## Phase 2: The All-Day Intelligence Upgrade

* **Epic:** Expand the agent's capabilities to trade intelligently throughout the entire trading day.

  * **Agent Definition: `Executor`**
    * **Intent:** To autonomously and safely execute trades based on signals, managing the full order lifecycle.
    * **ADK Class:** `google.adk.agents.BaseAgent` (custom agent implementing a deterministic Finite State Machine).
    * **ADK Sample Inspiration:** The FSM logic will be modeled after the state management patterns in the **`software-bug-assistant`** or **`customer-service`** samples.
    * **Callbacks:** A `RiskGovernorCallback` (`before_tool_callback`) will intercept all trade execution calls, a critical security pattern similar to the validation checks in the **`auto-insurance-agent`** sample.
    * **Knowledge Base Reference:** `ADR-0016`, `01_foundations/02_risk_management_architecture.md`.

---

## Phase 3: The Institutional Edge

* **Epic:** Achieve a near-institutional level of market analysis by integrating advanced data sources.

  * **Feature: Advanced Data Integration**
    * **Intent:** To enhance the `PreMarketAnalysis` agent by providing it with higher-fidelity data for scoring.
    * **ADK Sample Inspiration:** New tools for alternative data will follow the pattern of the **`fomc-research`** sample, which connects to specialized, external data sources.
    * **Knowledge Base References:** `04_tools_and_data/02_order_flow_data_feeds.md`, `04_tools_and_data/12_alternative_data_sec_filings.md`.
