# [STRATEGY: Scalping] Scalping

This document details Scalping, the highest-frequency day trading strategy, which profits from market microstructure inefficiencies. This strategy is only viable through full automation.

### [PRINCIPLE: Statistical_Edge] 1. Statistical Edge and Rationale

- **[WHAT]** Scalping exploits transient, structural inefficiencies within the market's mechanics, operating on a timescale of seconds or minutes. It aims to capture many small profits from minimal price moves.
- **[WHY]** The edge is derived from two primary sources:
    1. **[INEFFICIENCY: Bid_Ask_Spread] Capturing the Bid-Ask Spread:** The agent acts as a "miniature market maker," simultaneously placing buy and sell limit orders to capture the spread.
    2. **[INEFFICIENCY: Order_Flow_Imbalance] Fleeting Order Flow Imbalances:** The agent analyzes Level II and Time & Sales data to detect temporary, massive imbalances in buying or selling pressure that precede very short-term, directional price moves, and executes a trade to front-run slower participants.
- **[RISK: Adverse_Selection]** The primary risk is **adverse selection**: unknowingly trading with a more informed participant who is causing the imbalance, leading to immediate losses.

### [CONCEPT: Prerequisites] 2. Quantitative Prerequisites

- **[REQUIREMENT: High_Liquidity]** `Average Daily Volume > 5,000,000 shares`.
- **[REQUIREMENT: Tight_Spreads]** The bid-ask spread must be consistently **$0.01**.
- **[REQUIREMENT: Fee_Structure]** A **per-share commission** structure with low fees is mandatory. For market making, **liquidity-adding rebates** are required for profitability.

### [CONCEPT: Indicators] 3. Indicators for Scalping

Scalpers use fast-reacting indicators on very short timeframes (e.g., 1-minute charts).

- **[INDICATOR: Moving_Averages]** Fast EMAs (e.g., 9-period, 20-period) are used as dynamic support and resistance for quick bounce trades.
- **[INDICATOR: Oscillators]** Stochastics, MACD, and RSI are tuned to very short periods to identify micro-overbought/oversold conditions for fade scalps.
- **[INDICATOR: VWAP]** The Volume-Weighted Average Price is a key level. Scalpers trade bounces off VWAP or play for a quick cross and rejection.
- **[INDICATOR: Order_Flow_Imbalance]** An advanced indicator that directly measures the aggressive buy vs. sell orders from the tape, providing a real-time signal of short-term price pressure.

### [CONCEPT: AI_Architectures] 4. Specific, Programmable Scalping Architectures

1. **[ARCHITECTURE: Market_Making] Passive Market Making (Spread Capture):**
    - **[LOGIC:]** Continuously place bid and ask limit orders around a calculated mid-price. Actively manage inventory risk by "skewing" quotes to trade back towards a flat position.

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

### [CONCEPT: ADK_Implementation] 5. ADK Implementation: The Hybrid "Two-Speed Brain"

An `LlmAgent` is far too slow for direct scalping execution. The only viable architecture is a hybrid model that separates high-latency reasoning from low-latency execution.

- **Component 1: The High-Performance Execution Engine (C++ or Rust):** A lean, non-AI process that implements the core scalping logic. It subscribes directly to L2/Tape data feeds, sends orders, and exposes a simple control API.
- **Component 2: The Supervisory `LlmAgent` (ADK):** The ADK agent acts as the strategic "manager." It does **not** process high-frequency data. It consumes lower-frequency data (1-min bars, news, performance logs) to make high-level decisions, such as when to activate or deactivate the scalping module based on market regime.
- **Component 3: The Control Interface (`FunctionTool`):** The `LlmAgent` can only interact with the execution engine through a predefined, safety-checked set of `FunctionTool`s. This prevents the LLM from issuing dangerous or "hallucinated" commands.
  - `toggle_scalping_module(tool_context: ToolContext, strategy_name: str, state: bool)`
  - `update_risk_parameters(tool_context: ToolContext, max_inventory: int, order_size: int)`
  - `get_performance_report(tool_context: ToolContext) -> dict`

[SOURCE_ID: Intraday Scalping AI Architecture]
[SOURCE_ID: Expanded Day Trading Knowledge Base: Market Regimes, Indicators, and Strategies_chatGPT.md]
[SOURCE_ID: A Quantitative Framework for Algorithmic Day Trading: Regime Analysis, Pre-Market Evaluation, and Strategy Implementation]
