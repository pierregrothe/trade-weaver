# [STRATEGY: Scalping] Scalping

This document details Scalping, the highest-frequency day trading strategy, which profits from market microstructure inefficiencies.

### [PRINCIPLE: High_Frequency] Core Logic & Statistical Edge

- **[LOGIC: Definition]** Scalping exploits transient, structural inefficiencies like the **bid-ask spread** (liquidity provision) and temporary **order flow imbalances** (liquidity detection).
- **[LOGIC: High_Win_Rate]** The strategy relies on a very high win rate to accumulate hundreds of small wins into a significant net profit after costs.
- **[PARAMETER: Holding_Period]** Extremely short, lasting from seconds to a few minutes.

### [CONCEPT: Prerequisites] Quantitative Prerequisites

This strategy is only viable under specific, quantifiable conditions.

- **[REQUIREMENT: High_Liquidity]** `Average Daily Volume > 5,000,000 shares`.
- **[REQUIREMENT: Tight_Spreads]** The bid-ask spread must be consistently **$0.01**.
- **[REQUIREMENT: Fee_Structure]** A **per-share commission** structure is mandatory. For market making, **liquidity-adding rebates** are required for profitability.

### [CONCEPT: AI_Architectures] Specific Scalping Architectures for AI

1. **[ARCHITECTURE: Market_Making] Passive Market Making (Spread Capture):**
    - **[LOGIC:]** The agent simultaneously places bid and ask limit orders around a calculated mid-price, profiting from the spread and rebates. It must actively manage inventory risk by "skewing" quotes to trade back towards a flat position.
    - **[PSEUDOCODE: See Intraday Scalping AI Architecture document for full implementation]**

2. **[ARCHITECTURE: Order_Flow_Imbalance] Aggressive Order Flow Imbalance (Liquidity Taking):**
    - **[LOGIC:]** The agent scans the Level 2 order book for significant imbalances (e.g., bid volume is 3x ask volume) and executes an immediate market order to front-run the likely price move.
    - **[PSEUDOCODE: Imbalance_Scalp]**
        `FUNCTION execute_imbalance_scalp(ticker):`
        `// Continuously monitor the top N levels of the book`
        `WHILE True:`
        `bid_volume, ask_volume = get_level2_volume(ticker, depth=5)`
        `IF bid_volume > (ask_volume * 3.0):`
        `entry_price = execute_market_buy(ticker, position_size)`
        `// Immediately place OCO exit orders`
        `place_oco_sell_order(ticker, position_size, take_profit=entry_price+0.03, stop_loss=entry_price-0.02)`
        `WAIT_FOR_EXIT_FILL`
        `BREAK`

### [CONCEPT: ADK_Implementation] ADK Implementation: The Hybrid "Two-Speed Brain"

An LLM is far too slow for direct scalping execution. The only viable architecture is a hybrid model that separates high-latency reasoning from low-latency execution.

- **Component 1: The High-Performance Execution Engine (C++ or Rust):** A lean, non-AI process that implements the core scalping logic. It subscribes directly to L2/Tape data feeds, sends orders, and exposes a simple control API.
- **Component 2: The Supervisory `LlmAgent` (ADK):** The ADK agent acts as the strategic "manager." It does **not** process high-frequency data. It consumes lower-frequency data (1-min bars, news, performance logs) to make high-level decisions.
- **Component 3: The Control Interface (`FunctionTool`):** The `LlmAgent` can only interact with the execution engine through a predefined, safety-checked set of `FunctionTool`s. This prevents the LLM from issuing dangerous or "hallucinated" commands.
  - `toggle_scalping_module(tool_context: ToolContext, strategy_name: str, state: bool)`
  - `update_risk_parameters(tool_context: ToolContext, max_inventory: int, order_size: int)`
  - `get_performance_report(tool_context: ToolContext) -> dict`

[SOURCE_ID: Intraday Scalping AI Architecture]
