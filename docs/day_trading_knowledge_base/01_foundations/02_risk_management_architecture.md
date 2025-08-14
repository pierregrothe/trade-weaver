# [CONCEPT: Risk_Management] Risk Management Architecture: The Cornerstone of Longevity

This document codifies the multi-layered, hierarchical risk management system that governs every action to ensure long-term survival. These are absolute, non-negotiable protocols inspired by professional quantitative trading firms.

### [CONCEPT: Risk_Hierarchy] A Multi-Layered Defense System

Risk is managed in a hierarchy, from single-trade checks to system-wide circuit breakers. A failure at any layer can block a trade.

- **Layer 1: Pre-Trade & Single-Trade Constraints:** The first line of defense for every trade.
- **Layer 2: Portfolio-Level Constraints:** Manages aggregate and correlated risk across all open positions.
- **Layer 3: Dynamic & System-Level Controls:** Ultimate "circuit breakers" to protect the entire system during extreme market stress.

### [LAYER: 1] Layer 1: Single-Trade Protocols

- **[PROTOCOL: Max_Risk_per_Trade]** No single trade shall be sized to lose more than a fixed percentage of total account equity. The standard is **1%**. This is the most critical rule in risk management.
    - **Formula:** `Position Size = (Total_Account_Equity * Max_Risk_%) / (Entry_Price - Stop_Loss_Price)`
- **[PROTOCOL: ATR_Stop_Placement]** The initial stop-loss must be placed at a distance of at least **1.5 to 2.0 times the current 14-period Average True Range (ATR)** from the entry price. This adapts the stop-loss to the stock's specific volatility and helps avoid premature exits from market noise.
- **[PROTOCOL: Max_Position_Size]** A hard cap on the maximum dollar value of any single position (e.g., 25% of portfolio equity) to manage liquidity risk and prevent over-concentration.

### [LAYER: 2] Layer 2: Portfolio-Level Protocols

- **[PROTOCOL: Max_Gross_Exposure]** The sum of the absolute values of all long and short positions shall not exceed a predefined limit of account equity (e.g., **200%** for a 2:1 leveraged account). This controls the total capital deployed.
- **[PROTOCOL: Max_Net_Exposure]** The difference between total long and short positions shall not exceed a predefined limit (e.g., **+/- 75%**). This measures and controls the portfolio's overall directional market bias.
- **[PROTOCOL: Max_Sector_Exposure]** The net exposure to any single, predefined market sector (e.g., Technology, Healthcare) shall not exceed a hard limit (e.g., **25%** of account equity). This prevents catastrophic losses from a sector-wide event.
- **[PROTOCOL: Correlation_Matrix_Analysis]** The agent must periodically calculate the correlation matrix of all positions in the portfolio. If the overall portfolio correlation exceeds a certain threshold (e.g., 0.7), the agent should be prevented from adding new positions that would further increase this correlation.

### [LAYER: 3] Layer 3: System-Level Protocols (Circuit Breakers)

- **[PROTOCOL: Max_Daily_Drawdown]** A hard stop on the entire strategy for the day. If the total account equity drops by a predefined percentage (e.g., 3%) from the start of the day, all trading is halted, and all positions are liquidated.
- **[PROTOCOL: Trailing_Drawdown]** A hard stop on the entire strategy. A maximum trailing drawdown limit is set on the portfolio's equity (e.g., **5%**). If the current equity ever drops 5% below its highest-ever recorded value (the "high-water mark"), all trading is automatically halted.
- **[PROTOCOL: Volatility_Regime_Scaling]** The system must monitor a market-wide volatility index (e.g., the **VIX**). The risk parameters must be scaled dynamically based on the VIX reading:
    - `VIX < 20`: Normal risk parameters (e.g., 1% risk per trade).
    - `VIX 20-30`: Reduce risk parameters by 50% (e.g., 0.5% risk per trade).
    - `VIX > 30`: Cease all new trading and only manage existing positions.

[SOURCE_ID: Intraday Portfolio Risk Management, Section 4]
[SOURCE_ID: Day Trading AI Agent Research, Part II, Section 2.3]
