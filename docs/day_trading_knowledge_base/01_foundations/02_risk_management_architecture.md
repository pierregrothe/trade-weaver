# [CONCEPT: Risk_Management] Risk Management Architecture: The Cornerstone of Longevity

This document codifies the multi-layered, hierarchical risk management system that governs every action to ensure long-term survival. These are absolute, non-negotiable protocols inspired by professional quantitative trading firms, designed to be implemented as a sequential, programmatic validation pipeline.

### [CONCEPT: Risk_Hierarchy] A Multi-Layered Defense System

Risk is managed in a hierarchy, from single-trade checks to system-wide circuit breakers. A trade request must pass every layer of validation before it can be sent to the execution venue. A failure at any layer blocks the trade.

- **Layer 1: Pre-Trade & Single-Trade Constraints:** The first line of defense for every individual trade.
- **Layer 2: Portfolio-Level Constraints:** Manages aggregate and correlated risk across all open positions.
- **Layer 3: Dynamic & System-Level Controls:** Ultimate "circuit breakers" to protect the entire system during extreme market stress.

### [LAYER: 1] Layer 1: Single-Trade Protocols

#### [PROTOCOL: Max_Risk_per_Trade]
No single trade shall be sized to lose more than a fixed percentage of total account equity. The standard is **1%**. This is the most critical rule in risk management, ensuring mathematical survival over a long series of trades.

- **Rationale:** This rule ensures that even a long string of consecutive losses (e.g., 10 in a row) will not catastrophically deplete trading capital, allowing the strategy's positive expectancy to play out over time.
- **Dynamic Application:** While 1% is the *maximum* allowable risk, the agent can be programmed to risk less on lower-conviction setups (e.g., 0.5%) as determined by the output of its signal-generation model.
- **Formula:** `Position Size = (Total_Account_Equity * Max_Risk_%) / (abs(Entry_Price - Stop_Loss_Price))`
- **Example:**
    - Account Equity: $100,000
    - Max Risk %: 1% ($1,000)
    - Entry Price: $50.00
    - Stop-Loss Price: $48.00 (Risk per share = $2.00)
    - `Position Size = $1,000 / $2.00 = 500 shares`

#### [PROTOCOL: ATR_Stop_Placement]
The initial stop-loss must be placed at a distance determined by the instrument's recent volatility, using the **Average True Range (ATR)**.

- **Standard Multiple:** A multiple of **1.5 to 3.0 times the current 14-period ATR** is standard. This adapts the stop-loss to the stock's specific volatility and helps avoid premature exits from market noise.
- **The Multiplier Trade-off:** The choice of ATR multiple is a trade-off between a high win rate and a high risk/reward ratio. A smaller multiple (e.g., 1.5x) will result in a higher percentage of trades being stopped out, while a larger multiple (e.g., 3.0x) will give the trade more room to move but requires a smaller position size to adhere to the 1% rule.

### [LAYER: 2] Layer 2: Portfolio-Level Protocols

#### [PROTOCOL: Aggregate_Exposure_Limits]
- **Max Gross Exposure:** The sum of the absolute values of all long and short positions shall not exceed a predefined limit of account equity (e.g., **200%** for a 2:1 leveraged account). This controls the total capital deployed.
- **Max Net Exposure:** The absolute difference between total long and short positions shall not exceed a predefined limit (e.g., **+/- 75%**). This measures and controls the portfolio's overall directional market bias.
- **Example:** A portfolio with $150,000 long in tech stocks and $50,000 short in industrial stocks has a Gross Exposure of $200,000 and a Net Exposure of +$100,000.

#### [PROTOCOL: Correlated_Risk_Limits]
- **Max Sector Exposure:** The net exposure to any single, predefined market sector (e.g., Technology, Healthcare) shall not exceed a hard limit (e.g., **25%** of account equity).
- **Correlation Matrix Analysis:** The agent must periodically calculate the correlation matrix of the 5-minute returns of all open positions. If the average pairwise correlation exceeds a threshold (e.g., 0.7), a `CORRELATION_LIMIT_BREACH` flag is set, which prevents the execution of new trades in highly correlated assets.

### [LAYER: 3] Layer 3: System-Level Protocols (Circuit Breakers)

#### [PROTOCOL: Drawdown_Controls]
- **Max Daily Drawdown:** A hard stop on all trading for the day. This should be tiered:
    - **Soft Stop (`-1.5%`):** If account equity drops 1.5% from the start of the day, enter a "risk-off" mode: max risk per trade is halved to 0.5%, and high-risk strategies are disabled.
    - **Hard Stop (`-3.0%`):** If account equity drops 3%, all trading is halted, and all open positions are liquidated.
- **Trailing Drawdown:** A hard stop on the entire strategy. A maximum trailing drawdown limit is set on the portfolio's equity (e.g., **5%**). If the current equity ever drops 5% below its highest-ever recorded value (the "high-water mark"), all trading is automatically halted.

#### [PROTOCOL: Volatility_Regime_Scaling]
The system must monitor a market-wide volatility index (e.g., the **VIX**) and scale risk parameters dynamically.

- **VIX Level Scaling:**
  - `VIX < 18`: **Low Volatility.** Normal risk parameters (1% risk per trade).
  - `VIX 18-25`: **Medium Volatility.** Reduce risk parameters by 25% (0.75% risk per trade).
  - `VIX 25-35`: **High Volatility.** Reduce risk parameters by 50% (0.5% risk per trade).
  - `VIX > 35`: **Extreme Volatility.** Cease all new trading; only manage existing positions.
- **VIX Term Structure:** A VIX curve in **backwardation** (short-term VIX futures > long-term VIX futures) is a powerful predictor of imminent market stress. If this condition is met, the agent should apply the risk parameters from the next-highest volatility tier.

### [CONCEPT: Implementation_as_Code] Implementation as a Hierarchical Function

This entire architecture should be implemented as a single, sequential validation function that each trade request must pass through.

```python
# [PSEUDOCODE: Hierarchical_Risk_Validation]

FUNCTION validate_trade_risk(trade_request):
    # Layer 1 Checks
    IF NOT validate_single_trade_constraints(trade_request):
        RETURN REJECT(reason="Layer 1 Violation")

    # Layer 2 Checks
    IF NOT validate_portfolio_constraints(trade_request):
        RETURN REJECT(reason="Layer 2 Violation")

    # Layer 3 Checks
    IF NOT validate_system_constraints():
        RETURN REJECT(reason="Layer 3 Violation")

    # If all checks pass
    RETURN APPROVE(trade_request)
```

[SOURCE_ID: Intraday Portfolio Risk Management, Section 4]
[SOURCE_ID: Day Trading AI Agent Research, Part II, Section 2.3]
[SOURCE_ID: Dynamic Position Sizing Quantitative Analysis]
[SOURCE_ID: VIX Regime Filtering for Quantitative Strategies]