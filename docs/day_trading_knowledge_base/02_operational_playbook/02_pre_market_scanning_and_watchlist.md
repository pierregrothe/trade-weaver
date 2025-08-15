# [CONCEPT: Pre_Market_Analysis] Pre-Market Analysis: A Framework for Differentiating Continuation vs. Reversal Gaps

This document provides a detailed, actionable framework for the pre-market analysis pipeline. Its goal is to systematically filter the entire market down to a small, high-probability watchlist and to classify each candidate for either a momentum continuation ("Gap and Go") or a mean-reversion ("Gap Fade") strategy.

### [PIPELINE: Stage_1] Stage 1: Static Universe Filtering (Once Daily)

This initial filter creates the "Tradable Universe" by eliminating instruments that are structurally unsuitable for day trading.

- **[PARAMETER: Liquidity_Volume]** `Average Daily Volume (90-day) > 1,000,000 shares`.
- **[PARAMETER: Price_Range]** `Last Closing Price > $5.00 AND Last Closing Price < $200.00`.
- **[PARAMETER: Volatility]** `Average True Range (ATR, 14-day) > $0.50`.

### [PIPELINE: Stage_2] Stage 2: The Catalyst Imperative (7:00 AM - 9:00 AM ET)

The foundational requirement for a sustainable gap is a powerful, verifiable catalyst. This stage focuses on identifying the *why* behind the move.

- **[PRINCIPLE: Catalyst_Is_King]** A gap without a clear, fundamental reason is a low-probability setup. The agent must programmatically understand *why* a stock is moving.
- **[PROCESS: NLP_Pipeline]**
    1.  **[TASK: News_API_Query]** For each gapper, query a financial news API (e.g., Benzinga, EODHD) for all headlines within the last 18 hours.
    2.  **[TASK: Catalyst_Classification]** Process text with a domain-specific NLP model (e.g., FinBERT) to classify news into discrete types: `Earnings Beat/Miss`, `M&A Offer`, `FDA Approval/Rejection`, `Analyst Upgrade/Downgrade`, `Vague PR`.
    3.  **[TASK: Catalyst_Scoring]** Assign a quantitative strength score (1-10) to the catalyst. A Tier 1 catalyst (Earnings, M&A) implies institutional interest and a more stable trend. A Tier 3 catalyst (vague PR, social media hype) implies short-term retail interest and a more fragile, fade-prone move.

### [PIPELINE: Stage_3] Stage 3: Quantitative Filtering & Contextual Screening

This stage applies a multi-layered filtering process to the catalyst-driven candidates.

- **Layer 1: Baseline Metrics:**
    - **[PARAMETER: Gap_Percentage]** `| (PreMarket_Price / Previous_Close) - 1 | * 100 >= 4.0%`. Focuses on significant supply/demand imbalances.
    - **[PARAMETER: Relative_Volume_RVOL]** `Current Pre-Market Volume > 500% (5x)` of its historical average for that specific time of day. This is the single most important confirmation signal, indicating genuine, unusual interest.
- **Layer 2: Contextual Filters:**
    - **[FILTER: Float_as_Volatility_Multiplier]** Low-float stocks (< 20M shares) act as a volatility accelerant. For a "Gap and Go," a low float can create a short squeeze. For a "Gap Fade," a low float can lead to a more violent collapse.
    - **[FILTER: Sector_and_Market_Strength]** A top-down analysis of the broader market (SPY, QQQ) and sector ETFs (e.g., SMH, XLF) provides the crucial macro context. A stock gapping up in a strong sector has a tailwind; a stock gapping up in a weak sector is fighting the tide and is a prime fade candidate.

### [PIPELINE: Stage_4] Stage 4: Synthesized Checklists for Tactical Execution

This provides a final, objective scoring system before generating the output.

#### High-Probability "Gap and Go" (Continuation) Checklist

| Filter Category | Condition for High-Probability Continuation |
| :--- | :--- |
| **Catalyst** | Strong, verifiable Tier 1 or Tier 2 news (Earnings, M&A, FDA). |
| **Gap Percentage** | > 4% and < 25% (to avoid exhaustion). |
| **Relative Volume** | Pre-market RVOL > 5.0 and increasing into the open. |
| **Float** | Preferably low float (< 50M shares) to create supply squeeze potential. |
| **Sector/Market** | Broad market indices are bullish; stock is in a leading sector for the day. |
| **Intraday Action** | A clear break of the pre-market high on high volume OR a 1-minute ORB. |

#### High-Probability "Gap Fade" (Reversal) Checklist

| Filter Category | Condition for High-Probability Reversal |
| :--- | :--- |
| **Catalyst** | Weak/no catalyst, or a gap driven purely by broad market sentiment. |
| **Price Action** | The stock is overextended into a key daily resistance level. |
| **Relative Volume** | Low pre-market RVOL (< 2.0) OR climactic exhaustion volume at the open without price advance. |
| **Sector/Market** | Broad market indices are bearish or fading; stock is in a weak/lagging sector. |
| **Intraday Action** | Fails at the pre-market high, forms lower highs, and breaks below VWAP. |

### [OUTPUT: Structured_Object] Final Output for the AI Agent

The output is a ranked list of objects, now including a clear bias and key data points for the execution agent.

```json
[
  {
    "ticker": "XYZ",
    "rank": 1,
    "bias": "Continuation",
    "overall_score": 9.2,
    "catalyst_type": "Earnings Beat",
    "catalyst_score": 9.5,
    "sector_strength": "Leading",
    "pre_market_high": 115.50,
    "pre_market_low": 112.00,
    "key_daily_resistance": 120.00
  }
]
```

[SOURCE_ID: AI Day Trading Blueprint, Section 2]
[SOURCE_ID: The Definitive Day Trading Manual for the Québec-Based Trader, Part 1]
[SOURCE_ID: Gap Trading Strategies: Warrior vs. TraderLion Analysis]
[SOURCE_ID: Pre-Market Gap Analysis Strategy Synthesis]
