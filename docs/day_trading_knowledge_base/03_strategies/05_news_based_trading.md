# [STRATEGY: News_Based] News-Based Trading

This document details strategies for trading the volatility from news events. The core principle is to systematically exploit the market's inefficient processing of new information.

### [PRINCIPLE: Statistical_Edge] 1. Statistical Edge and Rationale

- **[WHAT]** News-based trading seeks to profit from the heightened volatility that occurs around significant news releases.
- **[WHY]** The edge is derived from several market inefficiencies:
    1. **[INEFFICIENCY: Latency_Arbitrage]** A pure speed advantage where an agent can process machine-readable news and trade microseconds before most human participants.
    2. **[INEFFICIENCY: Behavioral_Biases]** Exploiting predictable human over- and under-reactions (Post-Earnings Announcement Drift) to the news content.
    3. **[INEFFICIENCY: Limits_to_Arbitrage]** Profiting from price discovery catalyzed by the release of information.

### [CONCEPT: Programmable_Tactics] 2. Tactics for Scheduled, Quantitative Data

1. **[TACTIC: Volatility_Straddle] Volatility Straddle on Data Release:**
    - **[APPLICATION:]** For high-impact data releases with uncertain direction (e.g., FOMC).
    - **[EXECUTION:]** Between **T-10 and T-5 seconds** before the release, the agent places a Bracket OCO Order: a `BUY_STOP` order placed at `Pre-Release_High + (1.2 * ATR_1min)` and a `SELL_STOP` order at `Pre-Release_Low - (1.2 * ATR_1min)`.
    - **[OUTCOME:]** The data release causes a price surge, triggering one order and cancelling the other, capturing the initial momentum.

2. **[TACTIC: Data_Deviation] Data Deviation Trading:**
    - **[APPLICATION:]** Requires a machine-readable feed with Actual and Consensus values.
    - **[EXECUTION:]** The AI calculates a normalized "surprise" Z-Score: `Z = (Actual - Consensus) / StDev_of_Surprise`.
    - **[RULE:]** The agent trades based on the Z-score and historical correlations.

| [DATA: Economic_Release] | [ASSET: Primary_Impact] | [METRIC: Avg_Price_Move (60s) for +1σ Surprise] |
| :--- | :--- | :--- |
| **Non-Farm Payrolls (NFP)** | USD/JPY, EUR/USD | USD/JPY: **+15 to +25 pips** |
| **Consumer Price Index (CPI)** | E-mini S&P 500 (ES) | ES Futures: **-0.40% to -0.70%** (Higher inflation is bearish) |
| **Retail Sales** | USD/JPY, AUD/USD | USD/JPY: **+10 to +18 pips** |

### [CONCEPT: AI_Pipeline] 3. AI/NLP Pipeline for Unstructured News

1. **[PIPELINE: Stage_1] Ingestion:** Requires a low-latency **WebSocket** API delivering structured **Machine-Readable News (MRN)**.
2. **[PIPELINE: Stage_2] Hierarchical NLP Classification:** A multi-step process to extract meaning.
    - **NER:** First, a Named Entity Recognition model identifies all financial entities (tickers).
    - **Event Type Classification:** Next, a transformer model (e.g., FinBERT) classifies the event type (`M&A`, `FDA_Trial`, `Earnings`).
    - **Target-Based Sentiment:** Finally, a specialized model extracts the key parameters for that event type (e.g., EPS surprise, acquisition premium).
3. **[PIPELINE: Stage_3] Quantitative Market Impact Scoring (MIS):** The structured NLP output is distilled into a single, actionable score.
    - **[FORMULA: MIS]** `MIS = (w1*EventType) + (w2*Sentiment) + (w3*SourceCredibility) + (w4*NoveltyScore)`
    - `NoveltyScore` is calculated as `1 - max(Cosine_Similarity)` between the new headline's vector embedding and the embeddings of recent headlines stored in a vector database. This prevents trading on stale news.

### [CONCEPT: ADK_Implementation] 4. ADK Implementation Pipeline

- **[ADK: SequentialAgent] `NewsTradingPipelineAgent`**: A deterministic orchestrator that runs the following `FunctionTool`s in a strict sequence, passing data between them using `ToolContext.state`.
    1. **[TOOL: `NewsIngestionTool`]**: Fetches the latest headline, writes it to `tool_context.state`.
    2. **[TOOL: `NlpAnalysisTool`]**: Reads the headline from state, runs the NLP pipeline, and writes the structured analysis result back to state.
    3. **[TOOL: `SignalGenerationTool`]**: Reads the analysis result from state, calculates the MIS, and if it exceeds a threshold, returns the final, actionable trade signal (e.g., `{'signal': 'BUY', 'ticker': 'XYZ'}`).

[SOURCE_ID: News-Based Quantitative Trading Analysis]
