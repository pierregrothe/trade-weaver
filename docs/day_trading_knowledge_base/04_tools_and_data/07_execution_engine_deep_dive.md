# [CONCEPT: Execution_Engine] Algorithmic Trade Execution Deep Dive

This document details the critical microstructure of trade execution. It provides the AI agent with a sophisticated framework for order placement, cost estimation, and resilient broker API interaction.

### [SUBMODULE: Order_Placement] 1. A Decision-Theoretic Framework for Order Placement

The agent must dynamically select the order type that optimally balances price certainty and execution certainty.

- **[ORDER_TYPE: Market_Order]**
  - **WHAT:** An instruction to execute immediately at the best available price.
  - **WHY:** Use when **certainty of execution** is the absolute priority, typically for high-conviction, time-sensitive signals like a breakout.
  - **RISK:** **Slippage.** In volatile or thin markets, the fill price can be significantly worse than the expected price. It is a "blank check" for the price.
- **[ORDER_TYPE: Limit_Order]**
  - **WHAT:** An instruction to execute only at a specified price or better.
  - **WHY:** Use when **certainty of price** is the absolute priority, such as for mean-reversion entries at specific support/resistance levels or for profit-taking.
  - **RISK:** **Non-execution.** If the market does not reach the limit price, the trade may be missed entirely.
- **[ORDER_TYPE: Stop-Limit_Order]**
  - **WHAT:** A conditional order with two prices: a `stop_price` that triggers the order, and a `limit_price` that defines the worst acceptable fill price.
  - **WHY:** Offers a balance, providing control over slippage on stop-loss exits or breakout entries.
  - **RISK:** **Non-execution in a price gap.** If the market moves violently through both the stop and limit prices without trading in between, the order will be triggered but unfilled, leaving a losing position unprotected.
- **[ORDER_TYPE: Bracket_OCO_Order]**
  - **WHAT:** A composite order that, upon entry, automatically places a linked Stop-Loss and a Limit-based Profit-Target. If one is filled, the other is automatically cancelled (One-Cancels-Other).
  - **WHY:** **This is the mandatory, default order structure for the AI agent.** It programmatically enforces discipline and ensures every open position is protected from the moment of inception.

### [SUBMODULE: Slippage_Modeling] 2. Quantitative Slippage Modeling

The agent must estimate its transaction costs *before* placing a trade.

- **[MODEL: Volatility_and_Liquidity] A Practical Model for Market Orders:**
  - `Slippage_per_Share = (0.5 * Spread) + (k_vol * ATR) + (k_impact * (Order_Size / BBO_Size) * Spread)`
  - This formula combines the cost of crossing the spread, a buffer for volatility during execution latency, and a penalty for the order's size relative to the immediately available liquidity.
- **[MODEL: Square_Root_Impact] The Square Root Market Impact Model (for large orders):**
  - `Impact_USD = C * Volatility * sqrt(Order_Volume / Average_Daily_Volume)`
  - An institutional model used to estimate the price impact of orders that are a significant fraction of a stock's daily volume.

### [SUBMODULE: API_Resilience] 3. Resilient Broker API Interaction Patterns

- **[PATTERN: Token_Bucket] Rate Limiting with a Token Bucket Algorithm:** To avoid being blocked by the broker for exceeding API rate limits (e.g., 200 requests/minute), the agent must implement a client-side token bucket. This smooths out bursts of requests, ensuring compliance by forcing the agent to wait if its "bucket" of available API calls is empty.
- **[PATTERN: Exponential_Backoff] Error Handling with Exponential Backoff and Jitter:** When a retryable API error occurs (e.g., HTTP 503), the agent must not retry immediately. It must use an exponential backoff algorithm, waiting for progressively longer, randomized ("jittered") intervals between retries to avoid overwhelming the broker's servers.
- **[PATTERN: State_Machine] Order Management State Machine:** The agent must manage every order as a finite state machine (`PENDING_SUBMIT`, `SUBMITTED`, `PARTIALLY_FILLED`, `FILLED`, `CANCELLED`). This is especially critical for handling **partial fills**, which provide real-time information about market liquidity and must trigger a strategic re-evaluation of the remainder of the order.

[SOURCE_ID: Algorithmic Trade Execution Microstructure Guide]
