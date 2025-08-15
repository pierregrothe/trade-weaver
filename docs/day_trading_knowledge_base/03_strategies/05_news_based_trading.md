# [STRATEGY: News_Based] News-Based Trading

This document details strategies for trading the volatility from news events. The core principle is to systematically exploit the market's inefficient processing of new information using a quantitative, NLP-driven approach.

### [PRINCIPLE: Statistical_Edge] 1. Statistical Edge and Rationale

- **[WHAT]** News-based trading seeks to profit from the heightened volatility that occurs around significant, unscheduled news releases.
- **[WHY]** The edge is derived from several market inefficiencies:
    1. **[INEFFICIENCY: Latency_Arbitrage]** A pure speed advantage where an agent can process machine-readable news and trade microseconds before most human participants.
    2. **[INEFFICIENCY: Behavioral_Biases]** Exploiting predictable human over- and under-reactions (Post-Earnings Announcement Drift) to the news content.
    3. **[INEFFICIENCY: Catalyst_Momentum]** A strong catalyst attracts high volume and can create a durable intraday trend.

### [CONCEPT: AI_Pipeline] 2. AI/NLP Pipeline for Unstructured News

1.  **[PIPELINE: Stage_1] Ingestion:** Requires a low-latency **WebSocket** API delivering structured **Machine-Readable News (MRN)** from a provider like Benzinga or EODHD.
2.  **[PIPELINE: Stage_2] Hierarchical NLP Classification:** A multi-step process to extract meaning.
    - **NER:** First, a Named Entity Recognition model identifies all financial entities (tickers).
    - **Event Type Classification:** Next, a transformer model (e.g., FinBERT) classifies the event type (`M&A`, `FDA_Trial`, `Earnings`).
    - **Target-Based Sentiment:** Finally, a specialized model extracts the key parameters for that event type (e.g., EPS surprise, acquisition premium) and assigns a sentiment score.
3.  **[PIPELINE: Stage_3] Quantitative Market Impact Scoring (MIS):** The structured NLP output is distilled into a single, actionable score.
    - **[FORMULA: MIS]** `MIS = (w1*EventType) + (w2*Sentiment) + (w3*SourceCredibility) + (w4*NoveltyScore)`
    - `NoveltyScore` is calculated as `1 - max(Cosine_Similarity)` between the new headline's vector embedding and the embeddings of recent headlines stored in a vector database. This prevents trading on stale news.

### [CONCEPT: Actionable_Setups] 3. Actionable Setups from News Flow

- **[SETUP: Gap_and_Go]** For positive news with a high MIS score, if the stock gaps up and then breaks its pre-market high on high volume, it's a powerful "Gap and Go" entry signal.
- **[SETUP: Gap_Fade]** If a stock gaps up on weak news (low MIS score) or fails at the pre-market high, it may be a "Gap Fade" candidate, with the previous day's close as a potential target.
- **[SETUP: Intraday_Volatility]** For major, unexpected news during the trading day, an agent can place a volatility expansion order (e.g., a straddle using options) to profit from the expected increase in volatility regardless of direction.

### [CONCEPT: Risk_Management] 4. Risk Management for News Trades

- **[PRINCIPLE: Trade_the_Reaction]** A common pitfall is trading the news headline itself. The professional approach is to **"trade the reaction."** If a stock has great news but the price action is weak (e.g., fails to break the pre-market high, trades below VWAP), the negative price action overrides the positive headline. The agent's logic must prioritize price action over the news sentiment score for the final execution decision.
- **[PRINCIPLE: Volatility_Awareness]** News-driven moves are volatile. The agent should use wider stops (based on ATR) and potentially smaller position sizes. It may also be prudent to take partial profits into the initial surge and trail a stop on the remainder.

[SOURCE_ID: News-Based Quantitative Trading Analysis]
[SOURCE_ID: Expanded Day Trading Knowledge Base: Market Regimes, Indicators, and Strategies_chatGPT.md]
[SOURCE_ID: A Quantitative Framework for Algorithmic Day Trading: Regime Analysis, Pre-Market Evaluation, and Strategy Implementation]