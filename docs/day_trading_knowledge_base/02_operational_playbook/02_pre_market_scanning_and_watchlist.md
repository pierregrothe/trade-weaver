# [CONCEPT: Pre_Market_Analysis] Pre-Market Scanning and Watchlist Curation

The pre-market session is a critical, non-negotiable data processing pipeline that distills the market universe into a small, actionable watchlist. The goal is to focus exclusively on "stocks in play" that are exhibiting unusual activity driven by a clear catalyst.

### [PIPELINE: Stage_1] Stage 1: Static Universe Filtering

This is the broadest filter, run once daily to create the "Tradable Universe" by eliminating instruments that are fundamentally unsuitable for day trading.

- **[PARAMETER: Liquidity_Volume]** `Average Daily Volume (90-day) > 1,000,000 shares`.
- **[PARAMETER: Price_Range]** `Last Closing Price > $5.00 AND Last Closing Price < $200.00`.
- **[PARAMETER: Volatility]** `Average True Range (ATR, 14-day) > $0.50`.

### [PIPELINE: Stage_2] Stage 2: Pre-Market Dynamic Scan (Identifying Gappers)

This scan is executed in the pre-market session (7:00 AM - 9:25 AM ET) against the Tradable Universe to identify stocks demonstrating abnormal behavior.

- **[PRINCIPLE: Gappers]** Stocks that open at a price significantly different from their previous close are called "gappers." The gap signifies a supply/demand imbalance, usually caused by a post-market news catalyst.
- **[PARAMETER: Gap_Percentage]** `| (PreMarket_Price / Previous_Close) - 1 | * 100 >= 2.0%`. Gaps over 4% are considered particularly strong.
- **[PARAMETER: Pre_Market_Volume]** `PreMarket_Volume >= 100,000 shares by 9:00 AM ET`.
- **[PARAMETER: Relative_Volume_RVOL]** `Current Pre-Market Volume > 1000% (10x)` of its 30-day historical average for the same time of day.

#### Parameter Deep Dive for AI Logic

- **Why RVOL is critical:** Absolute volume is misleading (a stock trading 100k shares might be normal for it, but abnormal for another). **Relative Volume (RVOL)** normalizes this, showing what is truly unusual activity *for that specific stock*, making it a far superior signal for an AI.
- **Why Gap % matters:** The gap percentage is a direct measure of the initial supply/demand imbalance. A larger gap implies a more significant catalyst and a higher potential for a strong, sustained intraday trend.
- **Why Pre-Market Volume is a mandatory filter:** A gap on low volume is an unreliable signal. It indicates a lack of broad interest and has a high probability of "filling" (reverting to the previous close) immediately at the market open. High pre-market volume is the **conviction** behind the gap.

### [PIPELINE: Stage_3] Stage 3: Catalyst Identification and Scoring

- **[PRINCIPLE: Catalyst_Is_King]** A gap without a clear, fundamental reason is a low-probability setup. The AI agent must programmatically understand *why* a stock is moving.
- **[PROCESS: NLP_Pipeline]**
    1. **[TASK: News_API_Query]** For each gapper, query a financial news API (e.g., Benzinga) for all headlines within the last 18 hours.
    2. **[TASK: Catalyst_Classification]** Process text with a domain-specific NLP model (e.g., FinBERT) to classify news into discrete types: `Earnings Beat`, `M&A Offer`, `FDA Approval`, etc.
    3. **[TASK: Catalyst_Scoring]** Assign a quantitative strength score to the catalyst (e.g., 1-10) based on its type, urgency keywords, and source reliability.

### [PIPELINE: Stage_4] Stage 4: Watchlist Finalization and Ranking

- **[PRINCIPLE: Focus]** The agent must rank the filtered gappers to identify the "A+" setups and concentrate its focus and capital on the highest-probability opportunities.
- **[PROCESS: Ranking_Algorithm]** The identified gappers are ranked using an explicit, weighted formula:
  - `Ranking_Score = (Catalyst_Score * 0.40) + (RVOL_Score * 0.30) + (Gap_Score * 0.15) + (Chart_Clarity_Score * 0.15)`
  - `RVOL_Score` and `Gap_Score` should be normalized (e.g., on a scale of 1-10) before being used in the formula to ensure proper weighting.
  - `Chart_Clarity_Score` is a machine-learning or rule-based score that assesses the "cleanliness" of the pre-market price action.

### [OUTPUT: Structured_Object] Final Output for the AI Agent

The output of this entire pre-market pipeline is a structured list of objects, containing the top 5-10 ranked stocks, which is then passed to the execution modules.

**Example Output Object:**

```json
[
  {
    "ticker": "XYZ",
    "rank": 1,
    "overall_score": 9.2,
    "catalyst_type": "Earnings Beat",
    "catalyst_score": 9.5,
    "pre_market_high": 115.50,
    "pre_market_low": 112.00,
    "key_daily_resistance": 120.00
  },
  {
    "ticker": "ABC",
    "rank": 2,
    "overall_score": 8.8,
    "catalyst_type": "FDA Approval",
    "catalyst_score": 9.8,
    "pre_market_high": 54.20,
    "pre_market_low": 51.80,
    "key_daily_resistance": 55.00
  }
]```

[SOURCE_ID: AI Day Trading Blueprint, Section 2]
[SOURCE_ID: The Definitive Day Trading Manual for the Québec-Based Trader, Part 1]
