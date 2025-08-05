# [STRATEGY: Scalping] Scalping

This document details Scalping, the highest-frequency day trading strategy, which profits from market microstructure inefficiencies. This strategy is only viable through full automation.

### [PRINCIPLE: Statistical_Edge] 1. Statistical Edge and Rationale

- **[WHAT]** Scalping exploits transient, structural inefficiencies within the market's mechanics, operating on a timescale of seconds or milliseconds.
- **[WHY]** The edge is derived from two primary sources:
    1. **[INEFFICIENCY: Bid_Ask_Spread] Capturing the Bid-Ask Spread:** The agent acts as a "miniature market maker," simultaneously placing buy and sell limit orders to capture the spread, profiting from the cost of immediacy paid by other traders.
    2. **[INEFFICIENCY: Order_Flow_Imbalance] Fleeting Order Flow Imbalances:** The agent detects temporary, massive imbalances in the Limit Order Book (LOB) that precede very short-term, directional price moves, and executes a trade to front-run slower participants.
- **[RISK: Adverse_Selection]** The primary risk is **adverse selection**: unknowingly trading with a more informed participant who is causing the imbalance, leading to immediate losses.

### [CONCEPT: Prerequisites] 2. Quantitative Prerequisites

- **[REQUIREMENT: High_Liquidity]** `Average Daily Volume > 5,000,000 shares`.
- **[REQUIREMENT: Tight_Spreads]** The bid-ask spread must be consistently **$0.01**.
- **[REQUIREMENT: Fee_Structure]** A **per-share commission** structure is mandatory. For market making, **liquidity-adding rebates** are required for profitability.

### [CONCEPT: AI_Architectures] 3. Specific, Programmable Scalping Architectures

1. **[ARCHITECTURE: Market_Making] Passive Market Making (Spread Capture):**
    - **[LOGIC:]** Continuously place bid and ask limit orders around a calculated mid-price. Actively manage inventory risk by "skewing" quotes to trade back towards a flat position.
    - **[PSEUDOCODE: See Intraday Scalping AI Architecture document for full implementation]**

2. **[ARCHITECTURE: Order_Flow_Imbalance] Aggressive Order Flow Imbalance (Liquidity Taking):**
    - **[LOGIC:]** Scan the top levels of the L2 order book. If the volume on one side massively outweighs the other (e.g., `bid_volume > ask_volume * 3.0`), execute an immediate market order.
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

### [CONCEPT: ADK_Implementation] 4. ADK Implementation: The Hybrid "Two-Speed Brain"

An `LlmAgent` is far too slow for direct scalping execution. The only viable architecture is a hybrid model that separates high-latency reasoning from low-latency execution.

- **Component 1: The High-Performance Execution Engine (C++ or Rust):** A lean, non-AI process that implements the core scalping logic. It subscribes directly to L2/Tape data feeds and exposes a simple control API.
- **Component 2: The Supervisory `LlmAgent` (ADK):** The ADK agent acts as the strategic "manager." It does **not** process high-frequency data. It consumes lower-frequency data (1-min bars, news, performance logs) to make high-level decisions.
- **Component 3: The Control Interface (`FunctionTool`):** The `LlmAgent` can only interact with the execution engine through a predefined, safety-checked set of `FunctionTool`s. This prevents the LLM from issuing dangerous or "hallucinated" commands.
  - `toggle_scalping_module(tool_context: ToolContext, strategy_name: str, state: bool)`
  - `update_risk_parameters(tool_context: ToolContext, max_inventory: int, order_size: int)`
  - `get_performance_report(tool_context: ToolContext) -> dict`

[SOURCE_ID: Intraday Scalping AI Architecture]
