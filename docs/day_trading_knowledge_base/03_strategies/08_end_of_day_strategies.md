# [STRATEGY: End_of_Day] End-of-Day Trading Strategies

This document details the two primary, competing strategies for the final 30-60 minutes of the U.S. equity session: VWAP Reversion and Closing Momentum. The choice between these strategies is a function of market capitalization and real-time order imbalance data.

### [PRINCIPLE: Market_Dichotomy] 1. The Tale of Two Markets: A Market-Cap Dichotomy

The behavior of stocks in the final hour is not uniform; it is fundamentally split by market capitalization.

- **[BEHAVIOR: Large_Caps] Momentum-Reversal:** Large-capitalization stocks (e.g., S&P 500 components) are more prone to **mean reversion** in the final hour. Trends established earlier in the day tend to fade and reverse as institutions engage in profit-taking and liquidity provision.
- **[BEHAVIOR: Small_Caps] Continued-Momentum:** Small-capitalization stocks exhibit a much greater tendency for intraday trends to **persist and accelerate** into the close. This is due to lower liquidity, higher retail participation, and a greater susceptibility to short-covering cascades.

**Conclusion:** A successful end-of-day strategy *must* be bifurcated. This document focuses on the **Trend Continuation** strategy applicable to **small-cap stocks**.

### [STRATEGY: Trend_Continuation_into_Close] 2. The Small-Cap Trend Continuation Strategy

This strategy aims to identify and trade strong, established intraday trends in small-cap stocks during the final hour.

- **[UNIVERSE]** The strategy must be applied **exclusively** to small-capitalization U.S. equities (e.g., Russell 2000 members).
- **[ENTRY_TIMING]** The primary scan for entry signals is conducted at **15:00 ET**, with a final entry cutoff at 15:30 ET to allow sufficient time for the trend to play out.
- **[ENTRY_LOGIC: The_Confluence_Trigger]** A trade is triggered only when a confluence of filters confirms a robust trend:
    1.  **Price Action:** The stock has formed a clear series of higher highs and higher lows on the 5-minute chart since 13:00 ET.
    2.  **VWAP:** The current price is above the daily VWAP, and the VWAP slope is positive.
    3.  **Volume Profile:** The price is moving away from a High-Volume Node (HVN), indicating a path of least resistance.
    4.  **ADX:** The ADX(14) on the 5-minute chart is > 25, confirming statistically significant trend strength.

- **[RISK_MANAGEMENT]**
    - **Initial Stop-Loss:** Placed below the most recent significant swing low prior to entry. This anchors the risk to market structure.
    - **Trailing Stop (Recommended):** An **ATR-based trailing stop** (e.g., 2x ATR) is superior to a fixed R-multiple stop, as it dynamically adapts to the high volatility of the final hour.
    - **Exit Strategy:** All positions must be exited at or just before the 16:00 ET close, typically via a Market-on-Close (MOC) order.

### [STRATEGY: Closing_Momentum] 3. The Closing Auction Imbalance Strategy (Exception-Based)

This is a higher-risk, exception-based strategy that overrides the default VWAP Reversion approach when there is overwhelming evidence of a one-sided closing auction.

- **[RATIONALE]** The public dissemination of a large, directional closing auction imbalance in the final 10-15 minutes provides a powerful, actionable signal. It can trigger a self-fulfilling prophecy as arbitrageurs and momentum traders "front-run" the anticipated closing print.
- **[ENTRY_SIGNAL]**
    - **Primary Trigger:** A published closing imbalance representing a significant percentage of the stock's Average Daily Volume (e.g., >5%).
    - **Confirmation:** The stock price begins moving in the direction of the imbalance on accelerating volume.
- **[PROFIT_TARGET]** The closing auction price itself.
- **[EXECUTION]** This strategy requires aggressive, liquidity-demanding execution (e.g., marketable limit orders or POV algorithms) to chase the confirmed strength.