# [STRATEGY: News_Based] News-Based Trading

This document details strategies for trading the volatility from news events. The core principle is to systematically exploit the market's inefficient processing of new information.

### [PRINCIPLE: Statistical_Edge] 1. Statistical Edge and Rationale

- **[WHAT]** News-based trading seeks to profit from the heightened volatility that occurs around significant news releases, such as earnings reports, economic data, and M&A announcements.
- **[WHY]** The edge is derived from several market inefficiencies:
    1. **[INEFFICIENCY: Latency_Arbitrage]** A pure speed advantage where an agent can process machine-readable news and trade microseconds before most human participants.
    2. **[INEFFICIENCY: Behavioral_Biases]** Exploiting predictable human over- and under-reactions (Post-Earnings Announcement Drift) to the news content.
    3. **[INEFFICIENCY: Catalyst_Momentum]** A strong catalyst attracts high volume and can create a durable intraday trend.

### [CONCEPT: Catalyst_Identification] 2. Identifying and Filtering Catalysts

- **[PROCESS: Scanning]** The agent must use a pre-market scanner to identify stocks with fresh news and, critically, **high relative volume**. High relative volume is the market's confirmation that the news is impactful.
- **[PROCESS: Key_Levels]** For each stock with a catalyst, the agent must identify key technical levels: the pre-market high and low, and the previous day's high and low. These levels become the trigger points for trades.
- **[STRATEGY: Gap_and_Go]** For positive news, if the stock gaps up and then breaks its pre-market high on high volume, it's a powerful "Gap and Go" entry signal.
- **[STRATEGY: Gap_Fade]** If a stock gaps up on weak news or fails at the pre-market high, it may be a "Gap Fade" candidate, with the previous day's close as a potential target.

### [CONCEPT: AI_Pipeline] 3. AI/NLP Pipeline for Unstructured News

1. **[PIPELINE: Stage_1] Ingestion:** Requires a low-latency **WebSocket** API delivering structured **Machine-Readable News (MRN)**.
2. **[PIPELINE: Stage_2] Hierarchical NLP Classification:** A multi-step process to extract meaning.
    - **NER:** First, a Named Entity Recognition model identifies all financial entities (tickers).
    - **Event Type Classification:** Next, a transformer model (e.g., FinBERT) classifies the event type (`M&A`, `FDA_Trial`, `Earnings`).
    - **Target-Based Sentiment:** Finally, a specialized model extracts the key parameters for that event type (e.g., EPS surprise, acquisition premium) and assigns a sentiment score.
3. **[PIPELINE: Stage_3] Quantitative Market Impact Scoring (MIS):** The structured NLP output is distilled into a single, actionable score.
    - **[FORMULA: MIS]** `MIS = (w1*EventType) + (w2*Sentiment) + (w3*SourceCredibility) + (w4*NoveltyScore)`
    - `NoveltyScore` is calculated as `1 - max(Cosine_Similarity)` between the new headline's vector embedding and the embeddings of recent headlines stored in a vector database. This prevents trading on stale news.

### [CONCEPT: Risk_Management] 4. Risk Management for News Trades

- **[PRINCIPLE: Trade_the_Reaction]** A common pitfall is trading the news headline itself. The professional approach is to **"trade the reaction."** If a stock has great news but the price action is weak (e.g., fails to break the pre-market high, trades below VWAP), the negative price action overrides the positive headline.
- **[PRINCIPLE: Volatility_Awareness]** News-driven moves are volatile. The agent should use wider stops (based on ATR) and potentially smaller position sizes. It may also be prudent to take partial profits into the initial surge and trail a stop on the remainder.

### [CONCEPT: ADK_Implementation] 5. ADK Implementation Pipeline

- **[ADK: SequentialAgent] `NewsTradingPipelineAgent`**: A deterministic orchestrator that runs the following `FunctionTool`s in a strict sequence, passing data between them using `ToolContext.state`.
    1. **[TOOL: `NewsIngestionTool`]**: Fetches the latest headline, writes it to `tool_context.state`.
    2. **[TOOL: `NlpAnalysisTool`]**: Reads the headline from state, runs the NLP pipeline, and writes the structured analysis result back to state.
    3. **[TOOL: `SignalGenerationTool`]**: Reads the analysis result from state, calculates the MIS, and if it exceeds a threshold, returns the final, actionable trade signal (e.g., `{'signal': 'BUY', 'ticker': 'XYZ'}`).
    4. **[TOOL: `TradeExecutionTool`]**: Before executing, this tool must verify the price action against key levels (pre-market high/low, VWAP) to confirm the market's reaction aligns with the news sentiment.

[SOURCE_ID: News-Based Quantitative Trading Analysis]
[SOURCE_ID: Expanded Day Trading Knowledge Base: Market Regimes, Indicators, and Strategies_chatGPT.md]
[SOURCE_ID: A Quantitative Framework for Algorithmic Day Trading: Regime Analysis, Pre-Market Evaluation, and Strategy Implementation]
