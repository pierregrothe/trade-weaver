# [CONCEPT: Risk_Management] Risk Management Architecture: The Cornerstone of Longevity

This document codifies the multi-layered, hierarchical risk management system that governs every action to ensure long-term survival. These are absolute, non-negotiable protocols inspired by professional quantitative trading firms.

### [CONCEPT: Risk_Hierarchy] A Multi-Layered Defense System

Risk is managed in a hierarchy, from single-trade checks to system-wide circuit breakers. A failure at any layer can block a trade.

- **Layer 1: Pre-Trade & Single-Trade Constraints:** The first line of defense for every trade.
- **Layer 2: Portfolio-Level Constraints:** Manages aggregate and correlated risk across all open positions.
- **Layer 3: Dynamic & System-Level Controls:** Ultimate "circuit breakers" to protect the entire system during extreme market stress.

### [LAYER: 1] Layer 1: Single-Trade Protocols

- **[PROTOCOL: 1%_Rule]** No single trade shall be sized to lose more than 1% of total account equity if the stop-loss is hit.
- **[PROTOCOL: ATR_Stop_Placement]** The initial stop-loss must be placed at a distance of at least **1.5 times the current Average True Range (ATR)** from the entry price to avoid premature exits from market noise.
- **[PROTOCOL: Max_Position_Size]** A hard cap on the maximum dollar value of any single position to manage liquidity risk and prevent over-concentration.

### [LAYER: 2] Layer 2: Portfolio-Level Protocols

- **[PROTOCOL: Max_Gross_Exposure]** The sum of the absolute values of all long and short positions shall not exceed a predefined limit of account equity (e.g., **200%**). This controls the total capital deployed and overall leverage.
- **[PROTOCOL: Max_Net_Exposure]** The difference between total long and short positions shall not exceed a predefined limit (e.g., **+/- 75%**). This measures and controls the portfolio's overall directional market bias.
- **[PROTOCOL: Max_Sector_Exposure]** The net exposure to any single, predefined market sector (e.g., Technology, Healthcare) shall not exceed a hard limit (e.g., **25%** of account equity). This is the primary defense against the "five semiconductor stocks" problem.
- **[PROTOCOL: Max_Catalyst_Exposure]** The aggregate risk (sum of 1% risks) across all trades sharing the same primary catalyst (e.g., "CPI Data Release") shall not exceed a hard limit (e.g., **5%** of total equity).

### [LAYER: 3] Layer 3: System-Level Protocols (Circuit Breakers)

- **[PROTOCOL: Trailing_Drawdown]** A hard stop on the entire strategy. A maximum trailing drawdown limit is set on the portfolio's equity (e.g., **5%**). If the current equity ever drops 5% below its highest-ever recorded value (the "high-water mark"), all trading is automatically halted and positions are systematically liquidated.
- **[PROTOCOL: Volatility_Regime_Scaling]** The system must monitor a market-wide volatility index (e.g., the **VIX**). `IF VIX > 30 THEN` automatically scale down all risk parameters: reduce single-trade risk to 0.5%, reduce max gross exposure to 100%, etc. This forces the agent to be more conservative when the market is most dangerous.

[SOURCE_ID: Intraday Portfolio Risk Management, Section 4]
[SOURCE_ID: Day Trading AI Agent Research, Part II, Section 2.3]
